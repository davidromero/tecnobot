from chalice import Chalice
from chalicelib import add_campaigns, custom_responses, database
import boto3 as boto3
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION

app = Chalice(app_name='adwords_automation')
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/adwords', methods=['GET'])
def add_campaign():
    campaigns_list = get_app_db().list_all_items()
    for Item in campaigns_list:
        if (Item['payment_status'] is True) & (Item['active'] is False):
            add_campaigns.add(Item['business_name'])
            print('created campaign for name: ' + Item['business_name'])
    return custom_responses.get_campaigns(campaigns_list)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBCampaigns(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
