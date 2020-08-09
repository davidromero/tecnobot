import re


def get_payment_value(body):
    payment = {
        'transaction_number': get_match(r'\*\s*No\.\sTransacci\=C3\=B3n\s*\*[\r\n]+([^\r\n]+)', body),
        'payment_method': get_match(r'\*\s*Medio\sde\sPago\s*\*[\r\n]+([^\r\n]+)', body),
        'name': get_match(r'\*\s*Nombre\s*\*[\r\n]+([^\r\n]+)', body),
        'email': get_match(r'\*\s*Email\s*\*[\r\n]+([^\r\n]+)', body),
        'timestamp': get_match(r'\*\s*Fecha\sy\sHora\s*\*[\r\n]+([^\r\n]+)', body),
        'card_number': get_match(r'\*\s*Tarjeta\s*\*[\r\n]+([^\r\n]+)', body),
        'order_detail': get_match(r'\s*Producto\sCantidad\sPrecio\sSubtotal\s*[\r\n]+([^\r\n]+)', body),
        'total': get_match(r'\s*Total\sdel\spago\s*', body)
    }
    return payment


def get_match(regex, content):
    pattern = re.compile(rf'{regex}', re.MULTILINE | re.IGNORECASE)
    match = pattern.search(content)
    if match:
        return str(match.groups())[2:].replace(',', '').replace('(', '').replace(')', '').replace('\'', '').replace('>',
                                                                                                                    '')
    else:
        return ''
