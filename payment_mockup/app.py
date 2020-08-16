import requests
from chalice import Chalice
import json
from chalicelib.config import cors_config
import logging
from chalicelib import  custom_responses

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type'}

app = Chalice(app_name='payment_mockup')
app.log.setLevel(logging.DEBUG)


@app.route('/mockup', methods=['POST'], cors=cors_config)
def index():
    body = app.current_request.json_body
    response = http_request('https://2swpoc4hc4.execute-api.us-east-1.amazonaws.com/api/payment', body)
    if response['status'] == 201:
        response = http_request('https://oe5ye2mdwj.execute-api.us-east-1.amazonaws.com/api/adwords', body)
        if response['status'] == 201:
            return custom_responses.successful()
        else:
            return custom_responses.error_campaign_creation()
    else:
        return custom_responses.error_process_payment()


def http_request(endpoint, data):
    res = requests.post(endpoint,
                        data=json.dumps(data),
                        headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    return res.json()

