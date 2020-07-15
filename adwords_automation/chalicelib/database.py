import logging
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
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
