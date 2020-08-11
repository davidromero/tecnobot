import logging
from googleads import adwords, common
from chalicelib.adwords_actions import create_budget, create_campaign, create_add_group, create_add_extended_text

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def init_adwords(campaign):
    logging.info(campaign)
    client = adwords_client()
    logger.info(f"Starting campaign creation")
    logger.info(f"Creating a new budget of ${campaign['budget_amount']}")
    budget_id = create_budget(client)
    logger.info(f"Creating a new campaign for {campaign['business_name']}")
    campaign_id = create_campaign(client, budget_id, campaign['business_name'])
    logger.info(f"Campaign published with campaign ID: {str(campaign_id['value'][0]['id'])}")
    add_group_id = create_add_group(client, campaign_id['value'][0]['id'], campaign)
    logger.info(f"Add Group Addded with ID: {str(add_group_id)}")
    add_extended_id = create_add_extended_text(client, add_group_id, campaign)
    logger.info(f"Add Extended Created with ID: {str(add_extended_id)}")
    return campaign_id


def adwords_client():
    client = adwords.AdWordsClient.LoadFromStorage('chalicelib/credentials/googleads.yaml')
    client.cache = common.ZeepServiceProxy.NO_CACHE
    return client
