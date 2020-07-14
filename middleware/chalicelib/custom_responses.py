from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'}


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'Tecnobot webhook service running...'},
        headers=response_headers
    )


def post_response(new_item_id):
    if new_item_id is not None:
        return post_success(new_item_id)
    else:
        return post_fail()


def post_success(uid):
    return Response(
        status_code=201,
        body={
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Muchas gracias por la información. ¡Estamos listos para lanzar tu campaña publicitaria! Por último necesitamos que ingreses al siguiente enlace para ingresar tu método de pago y tu campaña publicitaria iniciará."
                        ]
                    },
                    "platform": "FACEBOOK"
                },
                {
                    "text": {
                        "text": [
                            "https://payment-link.com"
                        ]
                    },
                    "platform": "FACEBOOK"
                },
                {
                    "text": {
                        "text": [
                            "¡Eso sería todo! Si tienes alguna duda o pregunta puedes comunicarte directamente con nuestro equipo a info@tecnometro.net o puedes escribirnos a (502) 3517-7047"
                        ]
                    },
                    "platform": "FACEBOOK"
                }
            ]
        },
        headers=response_headers
    )


def post_fail():
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': 'Campaign could not be inserted.'
        },
        headers=response_headers
    )


def get_success(response):
    return Response(
        status_code=200,
        body={
            'status': 200,
            'payload': response
        },
        headers=response_headers
    )


def get_response(response, departament):
    if response is None:
        return not_found(departament)
    else:
        return get_success(response)


def not_found(departament):
    message = '{} not found'.format(departament)
    return Response(
        status_code=404,
        body={
            'status': 404,
            'payload': message
        },
        headers=response_headers
    )
