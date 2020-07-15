from datetime import datetime, timedelta
import logging
import uuid

from googleads import adwords, common

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def init_campaign(campaign):
    logger.info(f"Starting campaign creation")
    campaign_service, budget_service = get_services()
    logger.info(f"Creating a new budget of ${campaign['budget_amount']}")
    budget_id = create_budget(budget_service)
    logger.info(f"Creating a new campaign for {campaign['business_name']}")
    campaign_id = create_campaign(campaign_service, budget_id, campaign['business_name'])
    # logger.info(f"Creating a new ad for {campaign['website']}")
    logger.info('Campaign published')


def get_services():
    adwords_client = adwords.AdWordsClient.LoadFromStorage('chalicelib/credentials/googleads.yaml')
    adwords_client.cache = common.ZeepServiceProxy.NO_CACHE
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
            'name': f"{datetime.now().strftime('%Y%m%d')} - {campaign_name}",
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
