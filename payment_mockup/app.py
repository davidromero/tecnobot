from chalice import Chalice
import json
from chalicelib.config import cors_config
import requests

app = Chalice(app_name='payment_mockup')


@app.route('/mockup', methods=['POST'], cors=cors_config)
def index():
    body = app.current_request.json_body
    print(body)
    res = requests.post('https://2swpoc4hc4.execute-api.us-east-1.amazonaws.com/api/payment',
                        data=body,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json'})
#    if res.json()['status']:
#        if res.json()['status'] == 200:
    print(str(res))
    print(str(res.json()))
            # cambiar payment methods
#    else:
#        return {'Error': 'Error'}
#    return {'Error': 'Error'}

