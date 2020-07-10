import datetime
import json
import logging
import pytz
from chalicelib.validation import all_fields
from uuid import uuid4

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
        logger.info(f'Adding contact: {json.dumps(new_campaign)}')
        self._table.put_item(
            Item=new_campaign
        )
        return new_campaign.get('campaingid')


def make_campaign(campaign, username, uid):
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_contact = {
        'campaingid': uid,
        'active': True,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
    }
    for key in all_fields:
        value = campaign.get(key, EMPTY_FIELD)
        if isinstance(value, list):
            new_contact[key] = value
        elif value is '':
            new_contact[key] = '-'
        else:
            new_contact[key] = value.lower().strip()
    print("Making: " + json.dumps(new_contact))
    return new_contact
