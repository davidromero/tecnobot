import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


# TODO: Fix Mandatory phone_number and budget, cant lower() an Int

mandatory_fields = ['description', 'name', 'service', 'slogan', 'tittle', 'website']
non_editables = ['campaingid', 'created_by', 'created_timestamp', 'modified_by', 'modified_timestamp', 'active']
all_fields = ['description', 'location', 'name', 'service', 'slogan', 'tittle', 'website']


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
    if not (val_len_field(campaign, 'description') & val_len_field(campaign, 'name') & val_len_field(campaign,
                                                                                                     'service') \
            & val_len_field(campaign, 'slogan') & val_len_field(campaign, 'tittle')):
        return False
    if 'phone_number' in campaign.keys() and not validate_phone_number(campaign['phone_number']):
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
    if len(campaign[field]) < 3 or len(campaign[field]) > 99:
        logger.error(str + ' is invalid')
        return False
    return True
