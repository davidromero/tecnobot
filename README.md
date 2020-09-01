![CI](https://github.com/davidromero/tecnobot/workflows/CI/badge.svg)
# Tecnobot

<img src="https://github.com/davidromero/tecnobot/blob/master/docs/tecnobot.png?raw=true" width="558" height="507">


## Contents

- [Overview](#overview)
- [State and Scope](#state)
- [Services](#services)
- [Diagrams](#diagrams)
- [Requirements](#requirements)


## <a name="overview"></a>Overview
Web Services to create adds on Google-Adwords and process payments through Gmail.

## <a name="state"></a>State

**DEVELOPMENT** 

**Scope**
- Create and publish google ads programmatically from chatbot
- Process payments through notification email from third-party payment system.
- Integration Testing
- Create continuos deployment pipeline  

**Missing**
- IaC, specified the needed infrastructure on cloud formation
- Integrate payment services besides Pagalo.

**TODO**
- Save Keywords as a List on tecnobot_conversations
- Validate (website on CAP and number has a "-" or " ") fields format before processing them on campaigns
- DELETE process Diagram
- JWS authentication on Chalice


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

JSON for DELETE /adwords
```json
{
	"campaign_id": "3857fb28-3055"
}
```


### TecnoBots Payments

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

## <a name="diagrams"></a>Diagrams

### Sequence Diagram
<img src="https://github.com/davidromero/tecnobot/blob/master/docs/sequence_diagram.png?raw=true" width="637" height="354">

### ChaBot Overview Diagram
<img src="https://github.com/davidromero/tecnobot/blob/master/docs/Overview_diagram.png?raw=true" width="364" height="210">

### DB Diagram
<img src="https://github.com/davidromero/tecnobot/blob/master/docs/DB_diagram.png?raw=true" width="160" height="203">

### Conversations on Chatbot Diagram
<img src="https://github.com/davidromero/tecnobot/blob/master/docs/ConversationOnChatbot_diagram.png?raw=true" width="115" height="492">

### Payments on ChatBot Diagram
<img src="https://github.com/davidromero/tecnobot/blob/master/docs/PaymentOnChatBot_diagram.png?raw=true" width="181" height="585">

### Process Payment Diagram
<img src="https://github.com/davidromero/tecnobot/blob/master/docs/ProcessPayment_diagram.png?raw=true" width="120" height="491">

### Add Creation Diagram
<img src="https://github.com/davidromero/tecnobot/blob/master/docs/AddCreation_diagram.png?raw=true" width="62" height="345">

## <a name="requirements"></a>Requirements

- Python >= 3.6
- pip >= 20.0.2
- virtualenv >= 20.0.27
- AWS CLI >= 1.18.69
- chalice >= 1.15.1

