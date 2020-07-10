from os import environ
from chalice import CORSConfig

TABLE_NAME = environ.get('TABLE_NAME')
TABLE_NAME2 = environ.get('TABLE_NAME2')
AWS_DEFAULT_REGION = environ.get('AWS_DEFAULT_REGION')

cors_config = CORSConfig(
    allow_origin='*'
)
