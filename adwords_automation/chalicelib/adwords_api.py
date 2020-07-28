from datetime import datetime, timedelta
import logging
import uuid
import pytz
import argparse
import sys

from googleads import adwords, common
from chalicelib.add_group import create_add_group
from chalicelib.add_extended_text import create_add_extended_text
import google.ads.google_ads.client

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def init_adwords(campaign):
    logging.info(campaign)
    test_client = adwords.AdWordsClient.LoadFromStorage('chalicelib/credentials/googleads.yaml')
    test_client.cache = common.ZeepServiceProxy.NO_CACHE
    logger.info(f"Starting campaign creation")
    campaign_service, budget_service = get_services(test_client)
    logger.info(f"Creating a new budget of ${campaign['budget_amount']}")
    budget_id = create_budget(budget_service)
    logger.info(f"Creating a new campaign for {campaign['business_name']}")
    campaign_id = create_campaign(campaign_service, budget_id, campaign['business_name'])
    # logger.info(f"Creating a new ad for {campaign['website']}")
    logger.info('Campaign published with campaign ID: ' + str(campaign_id['value'][0]['id']))
    add_group_id = create_add_group(test_client, campaign_id['value'][0]['id'])
    logger.info('Add Group Addded with ID: ' + str(add_group_id))
    add_extended_id = create_add_extended_text(test_client, add_group_id)
    logger.info('Add Extended Created with ID: ' + str(add_extended_id))


def get_services(adwords_client):
    campaign_service = adwords_client.GetService('CampaignService', version='v201809')
    budget_service = adwords_client.GetService('BudgetService', version='v201809')
    return campaign_service, budget_service


def create_budget(budget_service):
    budget = {
        'amount': {
            'microAmount': '5000000'
        },
        'deliveryMethod': 'STANDARD',
        'isExplicitlyShared': False,
    }

    budget_operations = [{
        'operator': 'ADD',
        'operand': budget
    }]
    return budget_service.mutate(budget_operations)['value'][0]['budgetId']


def create_campaign(campaign_service, budget_id, campaign_name):
    operations = [{
        'operator': 'ADD',
        'operand': {
            'name': f"{(datetime.now(pytz.timezone('America/Guatemala')) + timedelta(365)).strftime('%m/%d/%Y, %H:%M:%S')} - {campaign_name}",
            'status': 'ELIGIBLE',
            'biddingStrategyConfiguration': {
                'biddingStrategyType': 'TARGET_SPEND'
            },
            'endDate': (datetime.now() + timedelta(365)).strftime('%Y%m%d'),
            'budget': {
                'budgetId': budget_id,
            },
            'advertisingChannelType': 'SEARCH'
        }
    }]
    return campaign_service.mutate(operations)
