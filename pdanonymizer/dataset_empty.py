import json


def load_raw_data(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return f.readlines()


def save_dataset(json_data, dataset_name="empty.json"):
    with open(dataset_name, 'w', encoding='UTF-8') as f:
        json.dump(json_data, f)


def transform_lines_json(raw_data):
    json_data = list()

    for line in raw_data:
        json_data.append([line, {'entities': []}])
        for item in line.split():
            json_data.append([item, {'entities': []}])
    return {"dataset": json_data}


def get_empty_dataset():
    raw_data = load_raw_data('empty.log')
    json_data = transform_lines_json(raw_data)
    save_dataset(json_data)


def main():
    get_empty_dataset()


if __name__ == "__main__":
    main()
