import logging
import boto3 as boto3
from chalice import Chalice
from chalicelib import database, custom_responses
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config
from chalicelib.mail import get_messages

app = Chalice(app_name='tecnobot_payments')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/payment', methods=['POST'], cors=cors_config)
def payment():
    body = app.current_request.json_body
    # new_item_id = get_app_db().add_item(patient=body)
    new_payment = get_messages(str(body["transaction_number"]))
    if new_payment:
        response = get_app_db().add_item(payment=new_payment)
        return custom_responses.post_response(new_payment)
    else:
        logger.info('Payment could not be saved')
        return custom_responses.post_response(new_payment=None)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBPayments(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
