from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type'}


def post_response(new_payment, message):
    if new_payment is not None:
        return post_success()
    else:
        return post_fail(message)


def post_success():
    return Response(
        status_code=201,
        body={
            'status': 201,
            'payload': 'Payment Accepted'
        },
        headers=response_headers
    )


def post_fail(message):
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': message
        },
        headers=response_headers
    )


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'tecnobot-payments service running...'},
        headers=response_headers
    )
