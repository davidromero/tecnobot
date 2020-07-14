import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class CampaignDB(object):
    def list_items(self, username):
        pass


class DynamoDBCampaigns(CampaignDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.info('Listing all campaigns')
        response = self._table.scan()
        return response['Items']
