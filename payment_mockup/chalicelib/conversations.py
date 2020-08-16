import datetime
import pytz
from uuid import uuid4

MARKETING_PACKAGES = {
    'MARKETING_COMBO_1': '',
    'MARKETING_COMBO_2': ''
}


def process_conversation(conversation):
    uid = str(uuid4())[:13]
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_campaign = {
        'campaingid': uid,
        'active': True,
        'payment_status': False,
        'created_timestamp': now,
        'slogan': conversation['slogan'],
        'phone': conversation['phone'],
        'website': conversation['website'],
        'location': conversation['location'],
        'history': conversation['history'],
        'search_terms': conversation['search_terms'],
        'business_name': conversation['business_name'],
        'description': conversation['description']
    }
    return new_campaign

def