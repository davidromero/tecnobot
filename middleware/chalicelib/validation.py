import logging
import re
from chalicelib.fields import *

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

mandatory_fields = [SLOGAN, BUDGET_AMOUNT, BUDGET_CURRENCY, SEARCH_TERMS, PHONE_NUMBER, WEBSITE, DESCRIPTION, \
                    BUSINESS_NAME, HISTORY, LOCATION]
non_editables = [CAMPAIGN_ID, USERNAME, ACTIVE, PAYMENT_STATUS, CREATED_TIMESTAMP]
all_fields = [CAMPAIGN_ID, USERNAME, ACTIVE, PAYMENT_STATUS, CREATED_TIMESTAMP, SLOGAN, BUDGET_AMOUNT, \
              BUDGET_CURRENCY, SEARCH_TERMS, PHONE_NUMBER, WEBSITE, DESCRIPTION, BUSINESS_NAME, HISTORY, \
              LOCATION]

budgets = ['5', '10', '15', '25', '50', '100' '200']


def validate_campaign_fields(new_campaign):
    if not has_mandatory_fields(new_campaign):
        logger.error("has_mandatory_fields")
        return False
    if not validate_mandatory_fields(new_campaign):
        logger.error("validate_mandatory_fields")
        return False
    if not validate_optional_fields(new_campaign):
        logger.error("validate_optional_fields")
        return False
    return True


def validate_optional_fields(campaign):
    if 'email' in campaign.keys() and not validate_email(campaign['email']):
        logger.error("Invalid email")
        return False
    return True


def validate_mandatory_fields(campaign):
    if not (val_len_field(campaign, SLOGAN) & val_len_field(campaign, BUDGET_CURRENCY) \
            & val_len_field(campaign, SEARCH_TERMS) & val_len_field(campaign, WEBSITE) \
            & val_len_field(campaign, DESCRIPTION) & val_len_field(campaign, BUSINESS_NAME) \
            & val_len_field(campaign, HISTORY) & val_len_field(campaign, LOCATION) & \
            val_budget_amount(campaign, BUDGET_AMOUNT)):
        return False
    if PHONE_NUMBER in campaign.keys() and not validate_phone_number(campaign[PHONE_NUMBER]):
        return False
    return True


def has_mandatory_fields(campaign):
    for mandatory_key in mandatory_fields:
        if mandatory_key not in campaign.keys():
            logger.error('Mandatory field missing: ' + mandatory_key)
            return False
        mandatory_value = campaign[mandatory_key].strip()
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
        print('Error in field ' + field)
        logger.error(str + ' is invalid')
        return False
    return True


def val_budget_amount(campaign, field):
    if campaign[field] in budgets:
        return True
    return False
