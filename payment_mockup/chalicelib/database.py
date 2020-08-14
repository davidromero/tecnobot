import datetime
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class CampaignsDB(object):
    def add_item(self, item):
        pass


class DynamoDBCampaigns(CampaignsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def add_item(self, campaign):
        logger.info('Adding new Campaign')
#        if validate_campaign_fields(new_campaign):
        logger.info(f'Inserting conversation: {json.dumps(campaign)}')
        self._table.put_item(
            Item=campaign
        )
        return campaign['campaingid']
#        else:
#            logger.info("Campaign creation is not valid")
#            return None


class ConversationDB(object):
    def get_item(self, psid, username):
        pass


class DynamoDBConversation(ConversationDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def get_item(self, psid, username=DEFAULT_USERNAME):
        logger.info(f'Getting conversation {psid}')
        response = self._table.get_item(
            Key={'psid': psid, }
        )
        if 'Item' in response:
            return response['Item']
        logger.error(f'Conversation {psid} not found')
        return None
