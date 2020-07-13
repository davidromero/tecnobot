import datetime
import json
import logging
import pytz
from chalicelib.validation import validate_campaign_fields, all_fields
from uuid import uuid4

logger = logging.getLogger()
logger.setLevel(logging.INFO)
EMPTY_FIELD = '-'


class CampaignsDB(object):
    def add_item(self, item):
        pass


class DynamoDBCampaigns(CampaignsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def add_item(self, campaign):
        logger.info('Adding new conversation')
        uid = str(uuid4())[:13]
        new_campaign = make_campaign(campaign, uid)
        if validate_campaign_fields(new_campaign):
            logger.info(f'Inserting conversation: {json.dumps(new_campaign)}')
            self._table.put_item(
                Item=new_campaign
            )
            return uid
        else:
            logger.info("Campaign creation is not valid")
            return None


def make_campaign(campaign, uid):
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    params = campaign['queryResult']['parameters']
    new_search_terms = str(params['search_term']).replace('\'', '').replace('[', '') \
        .replace(']', '')
    new_campaign = {
        'campaingid': uid,
        'active': True,
        'payment_status': False,
        'created_timestamp': now,
        'slogan': params['slogan'],
        'budget_amount': params['budget']['amount'],
        'budget_currency': params['budget']['currency'],
        'search_terms': new_search_terms,
        'phone': params['phone_number'],
        'website': params['website'],
        'description': params['description'],
        'business_name': params['business_name'],
        'history': params['history'],
        'location': params['location']['country'],
    }
    return new_campaign

