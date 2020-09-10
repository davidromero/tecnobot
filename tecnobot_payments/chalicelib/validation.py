def validate_transaction_number(transaction_number):
    if transaction_number:
        phone_number = str(transaction_number).strip(' ')
        if phone_number.isdigit() and len(phone_number) > 1:
            return True
    return False
