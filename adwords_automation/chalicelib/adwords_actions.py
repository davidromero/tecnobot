from datetime import datetime, timedelta
import pytz


def create_budget(adwords_client):
    budget_service = adwords_client.GetService('BudgetService', version='v201809')
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


def create_campaign(adwords_client, budget_id, campaign_name):
    campaign_service = adwords_client.GetService('CampaignService', version='v201809')
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
                            'microAmount': '5000000'
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
                    'headlinePart2': campaign['slogan'][:15],
                    'headlinePart3': 'Tel: ' + campaign['phone'],
                    'description': campaign['description'],
                    'description2': campaign['search_terms'],
                    'finalUrls': 'https://' + campaign['website'],
                },
                # Add status, ready to publish
                'status': 'ENABLE'
            }
        }
    ]
    ads = ad_group_ad_service.mutate(operations)

    return ads['value'][0]['ad']['id']
