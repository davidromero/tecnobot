import boto3 as boto3
from chalice import Chalice
from chalicelib import adwords_api, custom_responses, database
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config
from chalicelib.adwords_api import init_adwords
from chalicelib.adwords_actions import remove_campaign

app = Chalice(app_name='adwords_automation')
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/adwords', methods=['POST'])
def add_campaign():
    body = app.current_request.json_body
    campaigns_list = get_app_db().list_eligible_items()
    for campaign in campaigns_list:
        adwords_campaign_id = init_adwords(campaign)
        if adwords_campaign_id:
            print('adding adword_campaignid request')
            response = get_app_db().add_adwords_campaign(body['campaign_id'], adwords_campaign_id)
            # needed to handle response
        else:
            print('adwords_campaignid cant be added to campaign')
    return custom_responses.get_campaigns(campaigns_list)


@app.route('/adwords', methods=['DELETE'], cors=cors_config)
def delete_campaign():
    body = app.current_request.json_body
    adwords_response = remove_campaign(body['adwords_id'])
    print(adwords_response['value'][0]['status'])
    response = get_app_db().delete_campaign(body['campaign_id'])
    print(response)
    return 'yes'


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBCampaigns(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
