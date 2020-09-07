import datetime
import pytz
from uuid import uuid4

MARKETING_PACKAGES = {
    'MARKETING_COMBO_1': '2',
    'MARKETING_COMBO_2': '3',
    'MARKETING_COMBO_3': '4'
}


def process_conversation(conversation, username):
    uid = str(uuid4())[:13]
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_campaign = {
        'campaingid': uid,
        'active': True,
        'payment_status': True,
        'created_timestamp': now,
        'modified_timestamp': now,
        'modified_by': username,
        'budget_amount': get_budget_amount(conversation['marketing_package']),
        'budget_currency': 'USD',
        'slogan': conversation['slogan'],
        'phone': format_phone_number(conversation['phone']),
        'website': format_website(conversation['website']),
        'location': conversation['location'],
        'history': conversation['history'],
        'search_terms': conversation['search_terms'],
        'business_name': conversation['business_name'],
        'description': conversation['description']
    }
    return new_campaign


def get_budget_amount(package_type):
    return MARKETING_PACKAGES[package_type]


def format_phone_number(phone_number):
    return phone_number.replace(" ", "").replace("-", "")


def format_website(website):
    return website.lower()
