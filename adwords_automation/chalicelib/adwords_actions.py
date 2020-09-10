from datetime import datetime, timedelta
import pytz
from googleads import adwords, common


def adwords_client():
    client = adwords.AdWordsClient.LoadFromStorage('chalicelib/credentials/googleads.yaml')
    client.cache = common.ZeepServiceProxy.NO_CACHE
    return client


def create_budget(client, budget_amout):
    budget_service = client.GetService('BudgetService', version='v201809')
    # amount microAmount {One million is equivalent to one unit}
    budget = {
        'amount': {
            'microAmount': budget_amout
        },
        'deliveryMethod': 'STANDARD',
        'isExplicitlyShared': False,
    }

    budget_operations = [{
        'operator': 'ADD',
        'operand': budget
    }]
    return budget_service.mutate(budget_operations)['value'][0]['budgetId']


def create_campaign(client, budget_id, campaign_name):
    campaign_service = client.GetService('CampaignService', version='v201809')
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


def create_add_group(client, campaign_id, campaign):
    ad_group_service = client.GetService('AdGroupService', version='v201809')

    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': campaign_id,
            'name': campaign['business_name'],
            'status': 'ENABLED',
            'biddingStrategyConfiguration': {
                'bids': [
                    {
                        'xsi_type': 'CpcBid',
                        'bid': {
                            'microAmount': '1000000'
                        },
                    }
                ]
            },
            'settings': [
                {
                    'xsi_type': 'TargetingSetting',
                    'details': [
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'PLACEMENT',
                            'targetAll': 'false',
                        }
                    ]
                }
            ]
        }
    }]
    ad_groups = ad_group_service.mutate(operations)
    return ad_groups['value'][0]['id']


def add_campaign_targeting_criteria(client, campaign_id):
    campaign_criterion_service = client.GetService(
        'CampaignCriterionService', version='v201809')

    guatemala = {
        'xsi_type': 'Location',
        'id': '2320'
    }

    spanish = {
        'xsi_type': 'Language',
        'id': '1003'
    }

    criteria = [guatemala, spanish]

    operations = []
    for criterion in criteria:
        operations.append({
            'operator': 'ADD',
            'operand': {
                'campaignId': campaign_id,
                'criterion': criterion
            }
        })
    targeting_criteria = campaign_criterion_service.mutate(operations)
    return targeting_criteria


def create_add_extended_text(client, ad_group_id, campaign):
    ad_group_ad_service = client.GetService('AdGroupAdService', version='v201809')

    operations = [
        {
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'AdGroupAd',
                'adGroupId': ad_group_id,
                'ad': {
                    'xsi_type': 'ExpandedTextAd',
                    'headlinePart1': campaign['business_name'],
                    'headlinePart2': campaign['description'][:30],
                    'headlinePart3': campaign['slogan'][:30],
                    'description': campaign['history'][:90],
                    'description2': '',
                    'finalUrls': 'https://' + campaign['website'],
                },
                # Add status, ready to publish
                'status': 'ENABLE'
            }
        }
    ]
    ads = ad_group_ad_service.mutate(operations)
    return ads['value'][0]['ad']['id']


def add_keywords_to_add_group(client, ad_group_id, keyword_list):
    # Initialize appropriate service.
    ad_group_criterion_service = client.GetService(
        'AdGroupCriterionService', version='v201809')

    operations = construct_operations_keywords(ad_group_id, keyword_list)
    ad_group_criteria = ad_group_criterion_service.mutate(
        operations)['value']
    return ad_group_criteria


def construct_operations_keywords(ad_group_id, keyword_list):
    # Construct keyword ad group criterion object.
    operations = []
    for keyword in keyword_list:
        keyword_operand = {
            'xsi_type': 'BiddableAdGroupCriterion',
            'adGroupId': ad_group_id,
            'criterion': {
                'xsi_type': 'Keyword',
                'matchType': 'BROAD',
                'text': keyword
            }
        }
        operation = {
            'operator': 'ADD',
            'operand': keyword_operand
        }
        operations.append(operation)
    return operations


def remove_campaign(campaign_id):
    client = adwords_client()
    campaign_service = client.GetService('CampaignService', version='v201809')
    operations = [{
        'operator': 'SET',
        'operand': {
            'id': campaign_id,
            'status': 'REMOVED'
        }
    }]
    result = campaign_service.mutate(operations)
    return result
