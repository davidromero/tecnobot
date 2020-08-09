from os import environ

from chalice import CORSConfig

# dyamoDB
TABLE_NAME = environ.get('TABLE_NAME')
AWS_DEFAULT_REGION = environ.get('AWS_DEFAULT_REGION')
# admin email (Check Recieved mails)
EMAIL_ADDR = environ.get('EMAIL_ADDR')
PASSWORD = environ.get('PASSWORD')
# email from verified Pagalo ?
FROM_EMAIL = environ.get('FROM_EMAIL')
# email to notify admis
TO_ADDR = environ.get('TO_ADDR')
# SES SMTP AWS Creds
SMTP_USERNAME = environ.get('SMTP_USERNAME')
SMTP_PASSWORD = environ.get('SMTP_PASSWORD')
# SES Authorized email
SES_AUTH_FROM_EMAIL = environ.get('SES_AUTH_FROM_EMAIL')


cors_config = CORSConfig(
    allow_origin='*'
)

