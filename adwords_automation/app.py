from chalice import Chalice
from chalicelib import add_campaigns
from chalicelib import custom_responses

app = Chalice(app_name='adwords_automation')


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/add_campaign', methods=['GET'])
def add_campaign():
    add_campaigns.add()
    return {'hello': 'world'}

