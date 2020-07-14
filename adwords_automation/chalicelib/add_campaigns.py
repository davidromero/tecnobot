import datetime
import uuid
from os import environ
from googleads import adwords, oauth2

# OAuthClient
CLIENT_ID = environ.get('CLIENT_ID')
CLIENT_SECRET = environ.get('CLIENT_SECRET')
REFRESH_TOKEN = environ.get('REFRESH_TOKEN')

# Adwords API
DEVELOPER_TOKEN = environ.get('DEVELOPER_TOKEN')
USER_AGENT = environ.get('USER_AGENT')
CLIENT_CUSTOMER_ID = environ.get('CLIENT_CUSTOMER_ID')


def main(client):
    # Initialize appropriate services.
    campaign_service = client.GetService('CampaignService', version='v201809')
    budget_service = client.GetService('BudgetService', version='v201809')

    # Create a budget, which can be shared by multiple campaigns.
    budget = {
        'name': 'Interplanetary budget #%s' % uuid.uuid4(),
        'amount': {
            'microAmount': '5000000'
        },
        'deliveryMethod': 'STANDARD'
    }

    budget_operations = [{
        'operator': 'ADD',
        'operand': budget
    }]

    # Add the budget.
    budget_id = budget_service.mutate(budget_operations)['value'][0][
        'budgetId']

    # Construct operations and add campaigns.
    operations = [{
        'operator': 'ADD',
        'operand': {
            'name': 'Created within lambda #%s' % uuid.uuid4(),
            'status': 'ELIGIBLE',
            'biddingStrategyConfiguration': {
                'biddingStrategyType': 'MANUAL_CPC'
            },
            'endDate': (datetime.datetime.now() +
                        datetime.timedelta(365)).strftime('%Y%m%d'),
            # Note that only the budgetId is required
            'budget': {
                'budgetId': budget_id
            },
            'advertisingChannelType': 'DISPLAY'
        }
    }]
    campaigns = campaign_service.mutate(operations)

    # Display results.
    for campaign in campaigns['value']:
        print(('Campaign with name "%s" and id "%s" was added.'
               % (campaign['name'], campaign['id'])))


def add():
    oauth2_client = oauth2.GoogleRefreshTokenClient(
        CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

    adwords_client = adwords.AdWordsClient(
        DEVELOPER_TOKEN, oauth2_client, USER_AGENT,
        client_customer_id=CLIENT_CUSTOMER_ID)
    main(adwords_client)
