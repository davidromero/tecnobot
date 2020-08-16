from os import environ
from chalice import CORSConfig

cors_config = CORSConfig(
    allow_origin='*'
)


