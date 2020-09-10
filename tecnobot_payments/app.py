import logging
import boto3 as boto3
from chalice import Chalice
from chalicelib import database, custom_responses
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config
from chalicelib.mail import setup_mail
from chalicelib.validation import validate_transaction_number

app = Chalice(app_name='tecnobot_payments')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/', methods=['GET'], api_key_required=True)
def index():
    return custom_responses.get_base_res()


@app.route('/payment', methods=['POST'], cors=cors_config, api_key_required=True)
def payment():
    body = app.current_request.json_body
    if validate_transaction_number(body["transaction_number"]):
        val_payment = get_app_db().validate_payment(body["transaction_number"])
        if not val_payment:
            new_payment, error_message = setup_mail(str(body["transaction_number"]))
            if new_payment:
                response = get_app_db().add_item(payment=new_payment)
                return custom_responses.post_response(response, error_message)
            else:
                logger.info('Payment could not be saved')
                return custom_responses.post_response(None, error_message)
        else:
            logger.info(f'Payment {body["transaction_number"]} already processed')
            error_message = 'Payment already processed'
            return custom_responses.post_response(None, error_message)
    else:
        error_message = 'Bad Format on Transaction Number'
        logger.info(error_message + str(body["transaction_number"]))
        return custom_responses.post_response(None, error_message)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBPayments(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
