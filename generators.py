from faker import Faker


def get_name():
    faker = Faker()
    return faker.name()


def get_address():
    return Faker().address().replace("\n", " ")


def get_phone():
    return Faker().phone_number()


def get_birthday():
    return ".".join(Faker().date().split("-")[::-1])


def get_id():
    return Faker().ean()


def get_email():
    return Faker().email()


def generate_random(label):
    if label == "NAME":
        return get_name()
    elif label == "PHONE":
        return get_phone()
    elif label == "ID":
        return get_id()
    elif label == "ADDRESS":
        return get_address()
    elif label == "BIRTHDAY":
        return get_birthday()
    elif label == "EMAIL":
        return get_email()
