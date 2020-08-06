import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PaymentDB(object):

    def add_item(self, payment, username):
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
