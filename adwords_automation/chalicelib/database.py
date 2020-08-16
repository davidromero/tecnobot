import datetime
import logging
import pytz
import json
from boto3.dynamodb.conditions import Attr
from chalicelib import conversations

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class CampaignDB(object):
    def add_item(self, item):
        pass

    def list_items(self):
        pass

    def gte_item(self, uid):
        pass

    def update_item(self, uid, body):
        pass


class DynamoDBCampaigns(CampaignDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def add_item(self, conversation):
        logger.info('Adding new Campaign')
        new_campaign = conversations.process_conversation(conversation, username=DEFAULT_USERNAME)
        #        if validate_campaign_fields(new_campaign):
        logger.info(f'Inserting conversation: {json.dumps(new_campaign)}')
        self._table.put_item(
            Item=new_campaign
        )
        return new_campaign['campaingid']
#        else:
#            logger.info("Campaign creation is not valid")
#            return None

    def list_eligible_items(self):
        logger.info('Listing active paid campaign')
        response = self._table.scan(FilterExpression=Attr('active').eq(True) & Attr('payment_status').eq(True))
        return response['Items']

    def get_item(self, uid):
        logger.info(f'Getting Campaign: {uid}')
        item = self._table.get_item(Key={'campaingid': uid})['Item']
        if item is not None:
            return item
        else:
            logger.error(f'Campaign {uid} not found')
            return 404

    def delete_campaign(self, uid, username=DEFAULT_USERNAME):
        logger.info(f'Inactivating Campaign: {uid}')
        item = self._table.get_item(Key={'campaingid': uid})['Item']
        if item is not None:
            now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
            item['modified_by'] = username
            item['modified_timestamp'] = now
            item['adwords_campaignid'] = ''
            item['active'] = False
            response = self._table.put_item(Item=item)
            return response['ResponseMetadata']
        else:
            logger.error(f'Campaign {uid} not found')
            return 404

    def add_adwords_campaign(self, uid, adwords_campaignid, username=DEFAULT_USERNAME):
        logger.info(f'Adding Adwords CampaignId: {uid}')
        item = self._table.get_item(Key={'campaingid': uid})['Item']
        if item is not None:
            now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
            item['modified_by'] = username
            item['modified_timestamp'] = now
            item['adwords_campaignid'] = adwords_campaignid
            response = self._table.put_item(Item=item)
            return response['ResponseMetadata']
        else:
            logger.error(f'Campaign {uid} not found')
            return 404
