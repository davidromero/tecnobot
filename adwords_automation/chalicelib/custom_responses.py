from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type'}


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'adwords_automation service running...'},
        headers=response_headers
    )


def get_campaigns(campaign_list):
    if campaign_list is not None:
        return Response(
            status_code=200,
            body={
                'status': 200,
                'payload': campaign_list
            },
            headers=response_headers
        )
    else:
        return not_found(None)


def not_found(uid):
    message = '{} not found'.format(uid)
    return Response(
        status_code=404,
        body={
            'status': 404,
            'payload': message
        },
        headers=response_headers
    )
