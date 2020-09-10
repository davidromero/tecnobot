import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

available_locations = ['Mexico', 'Guatemala', 'El Salvador', 'Honduras', 'Nicaragua', 'Costa Rica', 'Panamá',
                       'Colombia']
available_packages = ['MARKETING_COMBO_1', 'MARKETING_COMBO_2', 'MARKETING_COMBO_3']
body_fields = ['business_name', 'description', 'history', 'location', 'marketing_package', 'phone', 'psid',
               'search_terms', 'slogan', 'website']


def validate_body(body):
    if validate_fields(body):
        valid = True
        valid = valid and validate_website(body['website'])
        valid = valid and validate_location(body['location'])
        valid = valid and validate_marketing_package(body['marketing_package'])
        return valid
    else:
        return False


def validate_fields(body):
    for body_key in body_fields:
        if body_key not in body.keys():
            logger.error('Mandatory field missing: ' + body_key)
            return False
        mandatory_value = body[body_key].strip()
        if mandatory_value is None:
            logger.error('Mandatory field is blank: ' + body_key)
            return False
    return True


def validate_website(website):
    if re.match(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}'
                r'(:[0-9]{1,5})?(\/.*)?$', website, re.IGNORECASE):
        return True
    return False


def validate_location(location):
    if location in available_locations:
        return True
    return False


def validate_marketing_package(marketing_package):
    if marketing_package in available_packages:
        return True
    return False

