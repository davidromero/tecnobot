from os import environ

from chalice import CORSConfig

TABLE_NAME = environ.get('TABLE_NAME')
AWS_DEFAULT_REGION = environ.get('AWS_DEFAULT_REGION')
EMAIL_ADDR = environ.get('EMAIL_ADDR')
PASSWORD = environ.get('PASSWORD')
FROM_EMAIL = environ.get('FROM_EMAIL')
TO_ADDR = environ.get('TO_ADDR')

cors_config = CORSConfig(
    allow_origin='*'
)

