import datetime
import logging
import pytz
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class CampaignDB(object):
    def list_items(self):
        pass

    def update_item(self, uid, body):
        pass


class DynamoDBCampaigns(CampaignDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_eligible_items(self):
        logger.info('Listing active paid campaigns')
        response = self._table.scan(FilterExpression=Attr('active').eq(True) & Attr('payment_status').eq(True))
        return response['Items']

    def delete_campaign(self, uid, username=DEFAULT_USERNAME):
        logger.info(f'Inactivating Campaign: {uid}')
        item = self._table.get_item(Key={'campaingid': uid})['Item']
        if item is not None:
            now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
            item['modified_by'] = username
            item['modified_timestamp'] = now
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
            print('Item to modified')
            print(item)
            return response['ResponseMetadata']
        else:
            logger.error(f'Campaign {uid} not found')
            return 404
