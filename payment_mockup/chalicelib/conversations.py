import datetime
import pytz
from uuid import uuid4


def process_conversation(conversation):
    uid = str(uuid4())[:13]
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_campaign = {
        'campaingid': uid,
        'active': True,
        'payment_status': False,
        'created_timestamp': now,
        'slogan': conversation['slogan'],
        'phoneNumber': conversation['phoneNumber'],
        'website': conversation['website'],
        'location': conversation['location'],
        'history': conversation['history'],
        'search_items': conversation['search_items'],
        'businessName': conversation['businessName'],
        'description': conversation['description']
    }
    return new_campaign
