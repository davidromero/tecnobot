import boto3 as boto3
from chalice import Chalice
from chalicelib import custom_responses, database
from chalicelib.config import TABLE_NAME, TABLE_NAME2, AWS_DEFAULT_REGION, cors_config

app = Chalice(app_name='middleware')
_DB = None
_DB2 = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/geo/{department}', methods=['GET'])
def get_location(department):
    department = department.replace("%20", " ")
    response = get_app_db2().get_item(department)
    return custom_responses.get_response(response, department)


@app.route('/middleware/campaign', methods=['POST'], cors=cors_config)
def add_campaing():
    body = app.current_request.json_body
    new_campaign = get_app_db().add_item(campaign=body)
    return custom_responses.post_response(new_campaign)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBCampaigns(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB

# TODO: refactor
def get_app_db2():
    global _DB2
    if _DB2 is None:
        _DB2 = database.DynamoDBGeo(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table("tecnobots_geo_dev")
        )
    return _DB2
