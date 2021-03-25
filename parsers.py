def txt_parsing(filename):
    with open(filename, 'r', encoding="UTF-8") as f:
        txt_data = [text.replace("\n", "") for text in f.readlines()]
    return txt_data


if __name__ == "__main__":
    txt_parsing("test.txt")
