import json
import os
import random


def load_full_dataset(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return json.load(f)


def save_dataset(filename, dataset):
    with open(filename, 'w', encoding='UTF-8') as f:
        json.dump({"dataset": dataset}, f)


def main():
    os.system("clear")
    print("Enter records amount for creating dataset:")
    records_amount = int(input())
    print("Loading full dataset...")
    dataset = load_full_dataset("converted.json")["dataset"]
    print("Handling full dataset...")
    random.shuffle(dataset)
    new_dataset = dataset[:records_amount]
    print("Enter filename for new dataset:")
    dataset_name = input()
    save_dataset(dataset_name, new_dataset)
    print("Done!")


if __name__ == "__main__":
    main()
