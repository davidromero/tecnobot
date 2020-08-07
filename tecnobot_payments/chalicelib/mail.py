import logging
import chalicelib.config as config
import io
import email.utils
import imaplib
import re
import smtplib

logger = logging.getLogger()
logger.setLevel(logging.INFO)

payment_fields = ('transaction_number', 'payment_method', 'name', 'email', 'timestamp', 'card_number', 'order_detail',
                  'total')


def setup_mail(transaction_number):
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(config.EMAIL_ADDR, config.PASSWORD)
    mail.list()
    mail.select('INBOX')
    result, data = mail.uid('search', None, 'ALL')
    mail, payment, error_message = get_messages(mail, data, transaction_number)
    mail.close()
    mail.logout()
    return payment, error_message


def get_messages(mail, data, transaction_number):
    error_message = ''
    i = len(data[0].split())
    new_payment = {}
    for x in range(i):
        email_message, latest_email_uid = get_body_mail(mail, data, x)
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                count = 0
                body = part.get_payload()
                new_payment = get_payment_value(body)
                if not correct_format(new_payment):
                    new_payment = {}
                    send_mail_notification(transaction_number, email_from)
                    error_message = f'Wrong Format on Mail from {email_from} Try Again!'
                    move_folder_mail_bad_format(mail, latest_email_uid)
                    return mail, new_payment, error_message
                count += 1
                if correct_format(new_payment) and (transaction_number in new_payment['transaction_number']) and \
                        (config.FROM_EMAIL in email_from):
                    return move_folder_mail(mail, latest_email_uid), new_payment, error_message
                new_payment = {}
    if not error_message:
        error_message = f'Payment Not Found for Transaction Number {transaction_number}'
    return mail, new_payment, error_message


def get_body_mail(mail, data, x):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    return email.message_from_string(raw_email_string), latest_email_uid


def get_payment_value(body):
    payment = {
        'transaction_number': get_match(r'\*\s*No\.\sTransacci\=C3\=B3n\s*\*[\r\n]+([^\r\n]+)', body),
        'payment_method': get_match(r'\*\s*Medio\sde\sPago\s*\*[\r\n]+([^\r\n]+)', body),
        'name': get_match(r'\*\s*Nombre\s*\*[\r\n]+([^\r\n]+)', body),
        'email': get_match(r'\*\s*Email\s*\*[\r\n]+([^\r\n]+)', body),
        'timestamp': get_match(r'\*\s*Fecha\sy\sHora\s*\*[\r\n]+([^\r\n]+)', body),
        'card_number': get_match(r'\*\s*Tarjeta\s*\*[\r\n]+([^\r\n]+)', body),
        'order_detail': get_match(r'\s*Producto\sCantidad\sPrecio\sSubtotal\s*[\r\n]+([^\r\n]+)', body),
        'total': get_match(r'\s*Total\sdel\spago\s*', body)
    }
    return payment


def get_match(regex, content):
    pattern = re.compile(rf'{regex}', re.MULTILINE | re.IGNORECASE)
    match = pattern.search(content)
    if match:
        return str(match.groups())[2:].replace(',', '').replace('(', '').replace(')', '')
    else:
        return ''


def get_content_line(lines, count):
    return lines[count + 1][2:].replace('\r', '').replace('\n', '')


def correct_format(payment):
    return all(field in payment for field in payment_fields)


def send_mail_notification(transaction_number, email_from):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config.EMAIL_ADDR, config.PASSWORD)
    msg = f"Payment with Transaction Number {transaction_number} cannot be Acepted, missing fields on Pagalo Mail {email_from}"
    server.sendmail(config.EMAIL_ADDR, config.TO_ADDR, msg)
    server.quit()


def move_folder_mail(mail, mail_uid):
    mail.uid('COPY', mail_uid, 'Paid')
    mail.uid('STORE', mail_uid, '+FLAGS', '(\Deleted)')
    mail.expunge()
    return mail

def move_folder_mail_bad_format(mail, mail_uid):
    mail.uid('COPY', mail_uid, 'Misc')
    mail.uid('STORE', mail_uid, '+FLAGS', '(\Deleted)')
    mail.expunge()
    return mail
