def txt_parsing(filename):
    with open(filename, 'r', encoding="UTF-8") as f:
        txt_data = [text.replace("\n", "") for text in f.readlines()]
    return txt_data


def csv_parsing(filename):
    with open(filename, 'r', encoding="UTF-8") as f:
        txt_data = [text.replace("\n", "").replace(',', '_') for text in f.readlines()]
    return txt_data

