import boto3 as boto3
from chalice import Chalice
from chalicelib import adwords_api, custom_responses, database
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION

app = Chalice(app_name='adwords_automation')
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/adwords', methods=['GET'])
def add_campaign():
    campaigns_list = get_app_db().list_eligible_items()
    for campaign in campaigns_list:
        adwords_api.init_adwords(campaign)
    return custom_responses.get_campaigns(campaigns_list)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBCampaigns(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
