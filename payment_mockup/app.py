import requests
from chalice import Chalice
import json
from chalicelib.config import cors_config
import logging

app = Chalice(app_name='payment_mockup')
app.log.setLevel(logging.DEBUG)


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

