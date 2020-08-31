![CI](https://github.com/davidromero/tecnobot/workflows/CI/badge.svg)
# Tecnobot

<img src="https://github.com/davidromero/tecnobot/blob/master/docs/tecnobot.png?raw=true" width="372" height="338">


## Contents

- [Overview](#overview)
- State and Scope
- [Services](#services)
- Diagrams
- Requirements


## <a name="overview"></a>Overview
Services to create adds on Google-Adwords and process payments through Gmail.


## <a name="services"></a>Services

### adwords_automation

| Method | URI Path        | Description                                                                        |
|--------|-----------------|------------------------------------------------------------------------------------|
| GET    | /               | Gets the service message                                                           |
| POST   | /adwords        | Create campaign in DynamoDB, create campaign, budget, add group and add in adwords |
| DELETE | /adwords        | Delete campaign from adwods and deactivate campaign in DynamoDB                    |


JSON for POST /adwords
```json
{
  "business_name": "Kaleidoscopic",
  "description": "Empower User to create easy Google Ads.",
  "history": "Create custom Ads from a ChatBot",
  "location": "Guatemala",
  "marketing_package": "MARKETING_COMBO_1",
  "phone": "40303202",
  "psid": "4078025715601000",
  "search_terms": "Ads, ChatBot, Marketing",
  "slogan": "Easy and Fast Ads",
  "website": "kaleidoscopic.dev"
}
```

JSON for DELTE /adwords
```json
{
	"campaign_id": "3857fb28-3055"
}
```


## TecnoBots Payments

| Method | URI Path        | Description                                              |
|--------|-----------------|----------------------------------------------------------|
| GET    | /               | Gets the service message                                 |
| POST   | /payment        | Process Payment from email and create payment in DynamoDB|

JSON for POST /payments
```json
{
  "transaction_number": "5954639929616444404274"
}
```
