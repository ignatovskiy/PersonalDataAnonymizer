import json
import random


pre_names = ["My ", "Our ", "His ", "Their ", "Her ", "This ", "Your ", '']

pre_name_words = ["name is ", 'is ']
pre_address_words = ["live in ", "address is ", "placed in ", "address: ", "location: ", "place: "]
pre_id_words = ["id is ", "passport num: ", "passport: ", "ID card number: ", "passport number: "]
pre_phone_words = ["call me at ", "phone: ", "contact us ", "phone us ", "back call ", "call "]
pre_birthday = ["birthday on ", "born in ", "dead in "]
pre_email = ["email ", "email: ", "email is ", "text me ", "contact us: ", "send me message "]

post_name_words = [" is my name", ' is me', ' has', ' waits', ' thinks', ' shows']
post_address_words = [" is my address", " is our location"]
post_id_words = [" is my ID", " is my passport num."]
post_phone_words = [" Call us.", " Phone us.", " Contact us."]
post_birthday = [" is my birthday", " is date", " is born date"]
post_email = [" is my email", " text me", " email us", " send message"]

random_vars = ["pre", "normal", "post"]


def load_raw_data(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return json.load(f)


def save_dataset(converted_data):
    with open("converted.json", 'w', encoding='UTF-8') as f:
        json.dump({"dataset": converted_data}, f)


def pre_adding(block, entity):
    if entity == "NAME":
        additional = random.choice(pre_names) + random.choice(pre_name_words)
    elif entity == "ID":
        additional = random.choice(pre_names) + random.choice(pre_id_words)
    elif entity == "PHONE":
        additional = random.choice(pre_names) + random.choice(pre_phone_words)
    elif entity == "EMAIL":
        additional = random.choice(pre_names) + random.choice(pre_email)
    elif entity == "BIRTHDAY":
        additional = random.choice(pre_names) + random.choice(pre_birthday)
    elif entity == "ADDRESS":
        additional = random.choice(pre_names) + random.choice(pre_address_words)
    else:
        additional = ""

    a_len = len(additional)
    converted_text = additional + str(block[entity])

    converted_entity = [converted_text,
                        {"entities": [[a_len, len(str(block[entity])) + a_len, str(entity)]]}]
    return converted_entity


def post_adding(block, entity):
    if entity == "NAME":
        additional = random.choice(post_name_words)
    elif entity == "ID":
        additional = random.choice(post_id_words)
    elif entity == "PHONE":
        additional = random.choice(post_phone_words)
    elif entity == "EMAIL":
        additional = random.choice(post_email)
    elif entity == "BIRTHDAY":
        additional = random.choice(post_birthday)
    elif entity == "ADDRESS":
        additional = random.choice(post_address_words)
    else:
        additional = ""
    converted_text = str(block[entity]) + additional

    converted_entity = [converted_text,
                        {"entities": [[0, len(str(block[entity])), str(entity)]]}]
    return converted_entity


def handling_data(pre_dataset):
    converted_dataset = list()

    for block in pre_dataset:
        for entity in block:
            condition = random.choice(random_vars)

            if condition == "pre":
                converted_entity = pre_adding(block, entity)
            elif condition == "post":
                converted_entity = post_adding(block, entity)
            else:
                converted_entity = [str(block[entity]),
                                    {"entities": [[0, len(str(block[entity])), str(entity)]]}]

            converted_dataset.append(converted_entity)
    return converted_dataset


def main():
    pre_dataset = load_raw_data("Dataset_Raw.json")
    converted_dataset = handling_data(pre_dataset)

    print(len(converted_dataset))
    random.shuffle(converted_dataset)
    save_dataset(converted_dataset)


if __name__ == "__main__":
    main()
