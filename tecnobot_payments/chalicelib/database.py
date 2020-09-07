import json
import logging
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PaymentDB(object):

    def add_item(self, payment, username):
        pass

    def validate_payment(self, transaction_number):
        pass


class DynamoDBPayments(PaymentDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def add_item(self, payment):
        logger.info('Adding new payment')
        logger.info(f'Adding payment: {json.dumps(payment)}')
        self._table.put_item(
            Item=payment
        )
        return payment

    def validate_payment(self, transaction_number):
        logger.info(f'Validating payment for transaction Number {transaction_number}')
        response = self._table.scan(
            FilterExpression=Attr('transaction_number').eq(transaction_number))
        logger.info(response)
        return response['Items']
