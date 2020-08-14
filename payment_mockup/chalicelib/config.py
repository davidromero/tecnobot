from os import environ
from chalice import CORSConfig

TABLE_NAME_CONVERSATION = environ.get('TABLE_NAME_CONVERSATION')
TABLE_NAME_CAMPAIGN = environ.get('TABLE_NAME_CAMPAIGN')

cors_config = CORSConfig(
    allow_origin='*'
)


