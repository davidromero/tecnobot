import logging
from googleads import adwords, common
from chalicelib.adwords_actions import create_budget, create_campaign, create_add_group, create_add_extended_text, \
    add_keywords_to_add_group, add_campaign_targeting_criteria

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def init_adwords(campaign, keywords):
    logging.info(campaign)
    client = adwords_client()
    logger.info(f"Starting campaign creation")
    logger.info(f"Creating a new budget of ${str(campaign['budget_amount']) + '000000'}")
    budget_id = create_budget(client, str(campaign['budget_amount']) + '000000')
    logger.info(f"Creating a new campaign for {campaign['business_name']}")
    campaign_id = create_campaign(client, budget_id, campaign['business_name'])
    logger.info(f"Campaign published with campaign ID: {str(campaign_id['value'][0]['id'])}")
    targeting_criteria = add_campaign_targeting_criteria(client, str(campaign_id['value'][0]['id']))
    logger.info(f"Targeting criteria added to Add Group{targeting_criteria['value']}")
    add_group_id = create_add_group(client, campaign_id['value'][0]['id'], campaign)
    logger.info(f"Add Group Added with ID: {str(add_group_id)}")
    ad_group_criteria = add_keywords_to_add_group(client, add_group_id, keywords_to_list(keywords))
    logger.info(f"Keywords added to Add Group with criteria")
    add_extended_id = create_add_extended_text(client, add_group_id, campaign)
    logger.info(f"Add Extended Created with ID: {str(add_extended_id)}")
    return campaign_id


def keywords_to_list(keywords):
    keywords_list = []
    words = keywords.split(',')
    for word in words:
        keywords_list.append(word)
    return keywords_list


def adwords_client():
    client = adwords.AdWordsClient.LoadFromStorage('chalicelib/credentials/googleads.yaml')
    client.cache = common.ZeepServiceProxy.NO_CACHE
    return client
