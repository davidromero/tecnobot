import datetime
import json
import logging
import pytz
from chalicelib.validation import validate_campaign_fields, all_fields
from uuid import uuid4
from chalicelib.fields import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class CampaignsDB(object):
    def add_item(self, contact, username):
        pass


class DynamoDBCampaigns(CampaignsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def add_item(self, campaign, username=DEFAULT_USERNAME):
        logger.info('Adding new contact')
        uid = str(uuid4())[:13]
        new_campaign = make_campaign(campaign, username, uid)
        if validate_campaign_fields(new_campaign):
            logger.info(f'Adding contact: {json.dumps(new_campaign)}')
            self._table.put_item(
                Item=new_campaign
            )
            return new_campaign.get(CAMPAIGN_ID)
        else:
            logger.info("Campaign creation is not valid")
            return None


def make_campaign(campaign, username, uid):
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_search_terms = str(campaign[QUERY_REQUEST][PARAMETERS]['search_term']).replace('\'', '').replace('[', '')\
    .replace(']', '')
    new_campaign = {
        'campaingid': uid,
        'username': username,
        'active': 'True',
        'payment_status': 'False',
        'created_timestamp': now,
        'slogan': campaign[QUERY_REQUEST][PARAMETERS][SLOGAN],
        'budge_amount': str(campaign[QUERY_REQUEST][PARAMETERS][BUDGET][AMOUNT]),
        'budge_currency': campaign[QUERY_REQUEST][PARAMETERS][BUDGET][CURRENCY],
        'search_terms': new_search_terms,
        'phone_number': campaign[QUERY_REQUEST][PARAMETERS][PHONE_NUMBER],
        'website': campaign[QUERY_REQUEST][PARAMETERS][WEBSITE],
        'description': campaign[QUERY_REQUEST][PARAMETERS][DESCRIPTION],
        'business_name': campaign[QUERY_REQUEST][PARAMETERS][BUSINESS_NAME],
        'history': campaign[QUERY_REQUEST][PARAMETERS][HISTORY],
        'location': campaign[QUERY_REQUEST][PARAMETERS][LOCATION][COUNTRY],
    }
    return new_campaign


class GeoDB(object):
    def get_item(self, department, username):
        pass


class DynamoDBGeo(GeoDB):
    def __init__(self, table_resource):
        self._table = table_resource

    # TODO: Fix DB, Primary Key name

    def get_item(self, department, username=DEFAULT_USERNAME):
        logger.info(f'Getting department {department}')
        response = self._table.get_item(
            Key={'departamento': department, }
        )
        if 'Item' in response:
            return response['Item']
        logger.error(f'Department {department} not found')
        return None

