import json
import os
import random


def load_full_dataset(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return json.load(f)


def save_dataset(filename, dataset):
    with open(filename, 'w', encoding='UTF-8') as f:
        json.dump({"dataset": dataset}, f)


def create(records_amount, output, dataset_filename="dataset.json"):
    print("Loading full dataset...")
    dataset = load_full_dataset(dataset_filename)["dataset"]
    print("Handling full dataset...")
    random.shuffle(dataset)
    new_dataset = dataset[:records_amount]
    save_dataset(output, new_dataset)
    print("Done!")


def create_dataset():
    os.system("clear")
    print("Enter filename of base dataset:")
    dataset_name = input()
    print("Enter records amount for creating dataset:")
    records_amount = int(input())
    print("Enter filename for new dataset:")
    output = input()
    create(records_amount, output, dataset_name)


def main():
    create_dataset()
