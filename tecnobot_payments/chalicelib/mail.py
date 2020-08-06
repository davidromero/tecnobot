import logging
import chalicelib.config as config
import io
import email.utils
import imaplib

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_messages(transaction_number):
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(config.EMAIL_ADDR, config.PASSWORD)
    mail.list()
    mail.select("INBOX")
    result, data = mail.uid('search', None, "ALL")
    i = len(data[0].split())
    new_payment = {}
    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))

        found = False
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload()
                buf = io.StringIO(body)
                lines = buf.readlines()
                count = 0
                new_payment = {}
                for line in lines:
                    if "No. Transacci=C3=B3n" in line:
                        if transaction_number in lines[count + 1].replace('\r', '').replace('\n', ''):
                            new_payment['transaction_number'] = lines[count + 1][2:].replace('\r', '').replace('\n', '')
                            found = True
                            logger.info('Payment found on mail')
                    if "Medio de Pago" in line and found:
                        new_payment['payment_method'] = get_content_line(lines, count)
                    if "Nombre" in line and found:
                        new_payment['name'] = get_content_line(lines, count)
                    if "Email" in line and found:
                        new_payment['email'] = get_content_line(lines, count)
                    if "Fecha y Hora" in line and found:
                        new_payment['timestamp'] = get_content_line(lines, count)
                    if "Tarjeta" in line and found:
                        new_payment['card_number'] = get_content_line(lines, count)
                    if "Producto Cantidad Precio Subtotal" in line and found:
                        new_payment['order_detail'] = get_content_line(lines, count)
                    if "Total del pago" in line and found:
                        new_payment['total'] = lines[count][2:].replace('\r', '').replace('\n', '')
                    count += 1
            else:
                continue
        print(new_payment)
        if len(new_payment) > 0 or x == i:
            logger.info('All [INBOX] mail Read')
            mail.close()
            mail.logout()
            return new_payment


def get_content_line(lines, count):
    return lines[count + 1].replace('\r', '').replace('\n', '').replace('>', '')
