import boto3 as boto3
import requests
from chalice import Chalice
import json
from chalicelib.config import cors_config, TABLE_NAME_CONVERSATION, TABLE_NAME_CAMPAIGN
import logging
from chalicelib import database, conversations

app = Chalice(app_name='payment_mockup')
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/mid', methods=['POST'], cors=cors_config)
def middleware():
    global _DB
    body = app.current_request.json_body
    new_campaign = conversations.process_conversation(body)
    print(str(new_campaign))
    campaign = get_app_db('campaign').add_item(new_campaign)
    _DB = None
    print(str(campaign))
    return {"yes": "yes"}
    # get conversation_item from psid
    # map fields to campaign_item
    # save item to tecnobot_campaing_dev


@app.route('/mockup', methods=['POST'], cors=cors_config)
def index():
    body = app.current_request.json_body
    print(body)
    response = http_request('https://2swpoc4hc4.execute-api.us-east-1.amazonaws.com/api/payment', body)
    print(response)
    if response['status'] == 201:
        http_request('https://oe5ye2mdwj.execute-api.us-east-1.amazonaws.com/api/adwords', body)
        res2 = requests.post('https://oe5ye2mdwj.execute-api.us-east-1.amazonaws.com/api/adwords',
                             data=json.dumps(body),
                             headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        print(res2.json())


def http_request(endpoint, data):
    res = requests.post(endpoint,
                        data=json.dumps(data),
                        headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    return res.json()


def get_app_db(bd_type):
    global _DB
    if _DB is None:
        if bd_type == 'conversation':
            print('conversation')
            _DB = database.DynamoDBConversation(
                boto3.Session().resource(service_name='dynamodb', region_name='us-east-1').Table(TABLE_NAME_CONVERSATION)
            )
        elif bd_type == 'campaign':
            print('campaign')
            _DB = database.DynamoDBCampaigns(
                boto3.Session().resource(service_name='dynamodb', region_name='us-east-1').Table(TABLE_NAME_CAMPAIGN)
            )
    return _DB

