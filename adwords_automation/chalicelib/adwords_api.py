from datetime import datetime, timedelta
import logging
import uuid
import pytz
import argparse
import sys

from googleads import adwords, common
import google.ads.google_ads.client

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
    logger.info('Campaign published with campaign ID: ' + str(campaign_id['value'][0]['id']))
    add_groupd_id = (create_add_group('6514825366', campaign_id['value'][0]['id'])).split('/')[3]
    logger.info('Add Group Addded with ID: ' + str(add_groupd_id))
    add_extended_id = create_add_extended_text('6514825366', add_groupd_id)
    logger.info('Add Extended Created with ID: ' + str(add_extended_id))


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


def create_add_group(customer_id, campaign_id):
    client = (google.ads.google_ads.client.GoogleAdsClient
              .load_from_storage('chalicelib/credentials/googleadsv4.yaml'))

    ad_group_service = client.get_service('AdGroupService', version='v4')
    campaign_service = client.get_service('CampaignService', version='v4')

    # Create ad group.
    ad_group_operation = client.get_type('AdGroupOperation', version='v4')
    ad_group = ad_group_operation.create
    ad_group.name.value = 'Kaleido Test 2 %s' % uuid.uuid4()
    ad_group.status = client.get_type('AdGroupStatusEnum', version='v4').ENABLED
    ad_group.campaign.value = campaign_service.campaign_path(
        customer_id, campaign_id)
    ad_group.type = client.get_type('AdGroupTypeEnum',
                                    version='v4').SEARCH_STANDARD
    ad_group.cpc_bid_micros.value = 10000000

    # Add the ad group.
    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id, [ad_group_operation])
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created ad group %s.' % ad_group_response.results[0].resource_name)
    return ad_group_response.results[0].resource_name


def create_add_extended_text(customer_id, ad_group_id):
    client = (google.ads.google_ads.client.GoogleAdsClient
              .load_from_storage('chalicelib/credentials/googleadsv4.yaml'))

    ad_group_ad_service = client.get_service('AdGroupAdService', version='v4')
    ad_group_service = client.get_service('AdGroupService', version='v4')

    ad_group_ad_operations = []

    # Create ad group ad.
    ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v4')
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group.value = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group_ad.status = client.get_type('AdGroupAdStatusEnum',
                                         version='v4').PAUSED

    # Set expanded text ad info
    final_url = ad_group_ad.ad.final_urls.add()
    final_url.value = 'http://www.example.com'
    ad_group_ad.ad.expanded_text_ad.description.value = 'Buy your tickets now!'
    ad_group_ad.ad.expanded_text_ad.headline_part1.value = (
        'Cruise {} to Mars {}')
    ad_group_ad.ad.expanded_text_ad.headline_part2.value = (
        'Best space cruise line')
    ad_group_ad.ad.expanded_text_ad.path1.value = 'all-inclusive'
    ad_group_ad.ad.expanded_text_ad.path2.value = 'deals'

    ad_group_ad_operations.append(ad_group_ad_operation)

    try:
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id, ad_group_ad_operations)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "{}" failed with status "{}" and includes the '
              'following errors:'.format(ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {}'.format(field_path_element.field_name))
        sys.exit(1)

    for result in ad_group_ad_response.results:
        print('Created ad group ad {}.'.format(result.resource_name))

    print('Created ad group ad ID: ' + ad_group_ad_response.results[0].resource_name)
    return ad_group_ad_response.results[0].resource_name
