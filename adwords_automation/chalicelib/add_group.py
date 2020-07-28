import uuid


def create_add_group(client, campaign_id):
    ad_group_service = client.GetService('AdGroupService', version='v201809')

    # Construct operations and add ad groups.
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': campaign_id,
            'name': 'Earth to Mars Cruises #%s' % uuid.uuid4(),
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
                    # Targeting restriction settings. Depending on the
                    # criterionTypeGroup value, most TargetingSettingDetail only
                    # affect Display campaigns. However, the
                    # USER_INTEREST_AND_LIST value works for RLSA campaigns -
                    # Search campaigns targeting using a remarketing list.
                    'xsi_type': 'TargetingSetting',
                    'details': [
                        # Restricting to serve ads that match your ad group
                        # placements. This is equivalent to choosing
                        # "Target and bid" in the UI.
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'PLACEMENT',
                            'targetAll': 'false',
                        },
                        # Using your ad group verticals only for bidding. This is
                        # equivalent to choosing "Bid only" in the UI.
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'VERTICAL',
                            'targetAll': 'true',
                        },
                    ]
                }
            ]
        }
    }]
    ad_groups = ad_group_service.mutate(operations)

    return ad_groups['value'][0]['id']
