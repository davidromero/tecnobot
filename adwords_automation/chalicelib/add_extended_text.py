import uuid


def create_add_extended_text(client, ad_group_id):
    ad_group_ad_service = client.GetService('AdGroupAdService', version='v201809')

    operations = [
        {
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'AdGroupAd',
                'adGroupId': ad_group_id,
                'ad': {
                    'xsi_type': 'ExpandedTextAd',
                    'headlinePart1': ('Cruise #%s to Mars'
                                      % str(uuid.uuid4())[:8]),
                    'headlinePart2': 'Best Space Cruise Line',
                    'headlinePart3': 'For Your Loved Ones',
                    'description': 'Buy your tickets now!',
                    'description2': 'Discount ends soon',
                    'finalUrls': ['http://www.example.com/'],
                },
                # Optional fields.
                'status': 'ENABLE'
            }
        }
    ]
    ads = ad_group_ad_service.mutate(operations)

    return ads['value'][0]['ad']['id']
