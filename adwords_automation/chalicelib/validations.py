def validate_business_name_descrip_slogan(business_name, description, slogan):
    if validate_word_medsize(business_name) and validate_word_medsize(description) and validate_word_medsize(slogan):
        return True
    return False


def validate_word_medsize(word):
    return word and 30 > len(word) > 2


def validate_history(word):
    return word and 90 > len(word) > 2


def validate_phone_number(number):
    if number:
        phone_number = str(number).strip(' ').replace('-', '')
        if phone_number.isdigit() and len(phone_number) > 1:
            return True
    return False
