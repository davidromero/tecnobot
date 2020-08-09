import logging
import chalicelib.config as config
from chalicelib.config import SMTP_USERNAME, SMTP_PASSWORD, SES_AUTH_FROM_EMAIL, TO_ADDR, FROM_EMAIL
from chalicelib.regex import get_payment_value
import email.utils
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    i = len(data[0].split())
    for x in range(i):
        error_message = ''
        email_message, latest_email_uid = get_body_mail(mail, data, x)
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain' and FROM_EMAIL in email_from:
                new_payment = get_payment_value(part.get_payload())
                if bad_format(new_payment):
                    error_message = f'Wrong Format on Mail from {email_from}, moved!'
                    notify(error_message, 'Bad Format Notification')
                    move_folder_mail_bad_format(mail, latest_email_uid)
                    break
                if (not bad_format(new_payment)) and (transaction_number in new_payment['transaction_number']):
                    msg = f'Payment Succesful for Transaction Number:\n{transaction_number} \n' \
                          f'Payment Info:\n{str(new_payment)}'
                    notify(msg, 'Acepted Payment Notification')
                    return move_folder_mail(mail, latest_email_uid), new_payment, error_message
        new_payment = {}
    if not error_message:
        error_message = f'Payment Not Found for Transaction Number {transaction_number}'
        notify(error_message, 'Not Found Payment Notification')
    return mail, new_payment, error_message


def get_body_mail(mail, data, x):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    return email.message_from_string(raw_email_string), latest_email_uid


def bad_format(payment):
    return all(value == '' for value in payment.values())


def notify(msg, subject):
    send_email(msg, subject)
    logger.info(msg)


def move_folder_mail(mail, mail_uid):
    mail.uid('COPY', mail_uid, 'Paid')
    mail.uid('STORE', mail_uid, '+FLAGS', '(\Deleted)')
    mail.expunge()
    logger.info(f'Mail from Payment moved to Paid')
    return mail


def move_folder_mail_bad_format(mail, mail_uid):
    mail.uid('COPY', mail_uid, 'Misc')
    mail.uid('STORE', mail_uid, '+FLAGS', '(\Deleted)')
    logger.info(f'Bad Formatted Mail moved to Misc')
    mail.expunge()
    return mail


def send_email(email_message, subject):
    server = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SES_AUTH_FROM_EMAIL
    message["To"] = SES_AUTH_FROM_EMAIL

    part1 = MIMEText(email_message, 'plain')
    message.attach(part1)
    server.sendmail(SES_AUTH_FROM_EMAIL, SES_AUTH_FROM_EMAIL, message.as_string())
