import logging
import chalicelib.config as config
import io
import email.utils
import imaplib

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_messages(transaction_number):
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(config.EMAIL_ADDR, config.PASSWORD)
    mail.list()
    mail.select('INBOX')
    result, data = mail.uid('search', None, 'ALL')
    i = len(data[0].split())
    new_payment = {}
    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        logger.info(
            f"Verifing emails from {config.FROM_EMAIL} Check the sender of the mail if Payment cannot be processed")

        found = False
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload()
                buf = io.StringIO(body)
                lines = buf.readlines()
                count = 0
                new_payment = {}
                for line in lines:
                    if 'No. Transacci=C3=B3n' in line:
                        if (transaction_number in lines[count + 1].replace('\r', '').replace('\n', '')) and \
                                (config.FROM_EMAIL in email_from):
                            new_payment['transaction_number'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                            found = True
                    elif 'Medio de Pago' in line:
                        new_payment['payment_method'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                    elif 'Nombre' in line:
                        new_payment['name'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                    elif 'Email' in line:
                        new_payment['email'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                    elif 'Fecha y Hora' in line:
                        new_payment['timestamp'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                    elif 'Tarjeta' in line:
                        new_payment['card_number'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                    elif 'Producto Cantidad Precio Subtotal' in line and found:
                        new_payment['order_detail'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                    elif 'Total del pago' in line:
                        new_payment['total'] = lines[count][2:].replace('\r', '').replace('\n', '')
                    count += 1
                if found:
                    mail.close()
                    mail.logout()
                    return new_payment
            else:
                continue
        if x == i:
            mail.close()
            mail.logout()
            return new_payment
