import json
from random import choice as rand
from random import shuffle


random_vars = ["pre", "normal", "post"]


def load_raw_data(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return json.load(f)


def save_dataset(converted_data):
    with open("../datasets/dataset.json", 'w', encoding='UTF-8') as f:
        json.dump({"dataset": converted_data}, f)


def pre_adding(block, entity):
    pre_dict = load_raw_data("contexts.json")
    additional = rand(pre_dict["first"]) + rand(pre_dict["pre"][entity])

    a_len = len(additional)
    converted_text = additional + str(block[entity])

    converted_entity = [converted_text,
                        {"entities": [[a_len, len(str(block[entity])) + a_len, str(entity)]]}]
    return converted_entity


def post_adding(block, entity):
    post_dict = load_raw_data("contexts.json")
    additional = rand(post_dict["post"][entity])

    converted_text = str(block[entity]) + additional

    converted_entity = [converted_text,
                        {"entities": [[0, len(str(block[entity])), str(entity)]]}]
    return converted_entity


def handling_data(pre_dataset):
    converted_dataset = list()

    for block in pre_dataset:
        for entity in block:
            condition = rand(random_vars)

            if condition == "pre":
                converted_entity = pre_adding(block, entity)
            elif condition == "post":
                converted_entity = post_adding(block, entity)
            else:
                converted_entity = [str(block[entity]),
                                    {"entities": [[0, len(str(block[entity])), str(entity)]]}]

            converted_dataset.append(converted_entity)
    return converted_dataset


def multi_handling_data(pre_dataset):
    converted_dataset = list()

    for block in pre_dataset:
        temp_block_items = list(block.items())
        shuffle(temp_block_items)
        temp_block = dict(temp_block_items)

        block_string = " ".join(list(temp_block.values()))
        entities_list = list()
        offset = 0

        for entity in temp_block:
            entities_list.append([offset, offset + len(str(temp_block[entity])), str(entity)])
            offset += len(str(temp_block[entity])) + 1

        converted_entity = [block_string, {"entities": entities_list}]
        converted_dataset.append(converted_entity)
    return converted_dataset


def convert_dataset(dataset_filename):
    pre_dataset = load_raw_data(dataset_filename)
    dataset_length = len(pre_dataset)
    converted_dataset = handling_data(pre_dataset[:dataset_length // 2])
    multi_converted_dataset = multi_handling_data(pre_dataset[dataset_length // 2:])
    converted_dataset.extend(multi_converted_dataset)
    shuffle(converted_dataset)
    save_dataset(converted_dataset)


def main(dataset_filename):
    convert_dataset(dataset_filename)