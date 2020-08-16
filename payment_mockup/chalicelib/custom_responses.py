from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type'}


def successful():
    return Response(
        status_code=201,
        body={
            'status': 201,
            'payload': "Payment and campaign creation process completed correctly"
        },
        headers=response_headers
    )


def error_process_payment():
    return Response(
        status_code=404,
        body={
            'status': 404,
            'payload': "Payment cannot be processed correctly"
        },
        headers=response_headers
    )


def error_campaign_creation():
    return Response(
        status_code=404,
        body={
            'status': 404,
            'payload': "Campaign cannot be created correctly"
        },
        headers=response_headers
    )
