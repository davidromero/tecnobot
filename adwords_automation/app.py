import logging
import boto3 as boto3
from chalice import Chalice
from chalicelib import adwords_api, custom_responses, database
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config
from chalicelib.adwords_api import init_adwords
from chalicelib.adwords_actions import remove_campaign

app = Chalice(app_name='adwords_automation')
_DB = None
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/adwords', methods=['POST'])
def add_campaign():
    response = {}
    body = app.current_request.json_body
    campaigns_list = get_app_db().list_eligible_items(body['campaign_id'])
    if campaigns_list:
        for campaign in campaigns_list:
            adwords_campaign_id = init_adwords(campaign)
            if adwords_campaign_id:
                logger.info(f'Adding adword_campaignid for campaign {campaign}')
                response = get_app_db().add_adwords_campaign(body['campaign_id'], adwords_campaign_id['value'][0]['id'])
            else:
                logger.info('Adwords_campaignid cant be added to campaign')
        if response['HTTPStatusCode'] == 200:
            logger.info('Adwords_campaignid added')
            return custom_responses.get_campaigns(campaigns_list, '')
        else:
            message = 'Adwords_campaignid cannot be added'
            logger.info(message)
            return custom_responses.get_campaigns(None, message)
    else:
        message = 'Cannot get Campaing to add, check DB for Campaign[active] status'
        logger.info(message)
        return custom_responses.get_campaigns(None, message)


@app.route('/adwords', methods=['DELETE'], cors=cors_config)
def delete_campaign():
    body = app.current_request.json_body
    item = get_app_db().get_item(body['campaign_id'])
    if item['adwords_campaignid']:
        adwords_response = remove_campaign(item['adwords_campaignid'])
        response = get_app_db().delete_campaign(body['campaign_id'])
        if response['HTTPStatusCode'] == 200:
            logger.info(f'Campaing was Deleted')
            return custom_responses.post_response(adwords_response['value'][0]['status'], '')
        else:
            error_message = 'Campaign Could not be Deleted'
            logger.info(error_message)
            return custom_responses.post_response(None, error_message)
    else:
        error_message = 'Campaign is already Deleted'
        logger.info(error_message)
        return custom_responses.post_response(None, error_message)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBCampaigns(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
