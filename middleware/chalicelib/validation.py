import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

mandatory_fields = ['slogan', 'budget_amount', 'budget_currency', 'search_terms', 'phone', 'website', 'description', \
                    'business_name', 'history', 'location']
non_editables = ['campaingid', 'active', 'payment_status', 'created_timestamp', 'modified_timestamp']
all_fields = ['campaingid', 'slogan', 'budget_amount', 'budget_currency', 'search_terms', 'phone', 'website',
              'description', 'business_name', 'history', 'location']

budgets = [5, 10, 15, 25, 50, 100, 200]


def validate_campaign_fields(new_campaign):
    if not has_mandatory_fields(new_campaign):
        return False
    if not validate_mandatory_fields(new_campaign):
        return False
    return True


def validate_optional_fields(campaign):
    if 'email' in campaign.keys() and not validate_email(campaign['email']):
        logger.error("Invalid email")
        return False
    return True


# TODO Fix using a loop
def validate_mandatory_fields(campaign):
    if not (val_len_field(campaign, 'slogan') & val_len_field(campaign, 'budget_currency') \
            & val_len_field(campaign, 'search_terms') & val_len_field(campaign, 'website') \
            & val_len_field(campaign, 'description') & val_len_field(campaign, 'business_name') \
            & val_len_field(campaign, 'history') & val_len_field(campaign, 'location') & \
            val_budget_amount(campaign)):
        return False
    if 'phone' in campaign.keys() and not validate_phone_number(campaign['phone']):
        return False
    return True


def has_mandatory_fields(campaign):
    for mandatory_key in mandatory_fields:
        if mandatory_key not in campaign.keys():
            logger.error('Mandatory field missing: ' + mandatory_key)
            return False
        if isinstance(campaign[mandatory_key], str):
            mandatory_value = campaign[mandatory_key].strip()
        else:
            mandatory_value = campaign[mandatory_key]
        if mandatory_value == '-' or None:
            logger.error('Mandatory field is blank: ' + mandatory_key)
            return False
    return True


def validate_email(email):
    if email is '-':
        return True
    if re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email, re.IGNORECASE):
        return True
    return False


def validate_phone_number(phone_number):
    phone_number = str(phone_number).strip(' ')
    if phone_number.isdigit() and len(phone_number) == 8:
        return True
    return False


def val_len_field(campaign, field):
    if len(campaign[field]) < 3 or len(campaign[field]) > 130:
        logger.error(field + ' is invalid')
        return False
    return True


def val_budget_amount(campaign):
    if not campaign['budget_amount'] in budgets:
        logger.error(f"{campaign['budget_amount']} is not in the supported budgets")
        return False
    return True
