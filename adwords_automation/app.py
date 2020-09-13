import logging
import boto3 as boto3
from chalice import Chalice
from chalicelib.adwords_api import init_adwords
from chalicelib import custom_responses, database
from chalicelib.adwords_actions import remove_campaign
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config
from chalicelib.validations import validate_body

app = Chalice(app_name='adwords_automation')
_DB = None
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/', methods=['GET'], api_key_required=True)
def index():
    return custom_responses.get_base_res()


@app.route('/adwords', methods=['POST'], api_key_required=True)
def add_campaign():
    response = {}
    body = app.current_request.json_body
    logger.info(f'Body recieved {body}')
    if not validate_body(body):
        message = 'Error on Body validation'
        return custom_responses.get_campaigns(None, message)
    campaign = get_app_db().list_eligible_items(body['psid'])
    if not campaign:
        new_campaign = get_app_db().add_item(body)
        adwords_campaign_id = init_adwords(new_campaign, body['search_terms'])
        if adwords_campaign_id:
            logger.info(f'Adding adword_campaignid for campaign {campaign}')
            response = get_app_db().add_adwords_campaign(new_campaign['campaingid'],
                                                         adwords_campaign_id['value'][0]['id'])
        else:
            logger.info('Adwords_campaignid cant be added to campaign')
        if response['HTTPStatusCode'] == 200:
            logger.info('Adwords_campaignid added')
            message = 'Campaign successfully created'
            return custom_responses.get_campaigns(campaign, message)
        else:
            message = 'Adwords_campaignid cannot be added'
            logger.info(message)
            return custom_responses.get_campaigns(None, message)
    else:
        message = 'Campaign already processed'
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
