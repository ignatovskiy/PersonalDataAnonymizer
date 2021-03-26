import json
from pathlib import Path
import random
import time

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding

from parsers import *
from generators import generate_random


def log(log_type, text):
    logs_type = {"info": "[I]: ",
                 "good": "[+]: ",
                 "bad": "[-]: ",
                 "error": "[X]: ",
                 "ask": "[?]: "}
    print(f"{logs_type[log_type]}{text}")


def create_model():
    return spacy.blank("en")


def load_model(model_dir_path):
    return spacy.load(model_dir_path)


def load_train_dataset(dataset_name):
    with open(dataset_name, "r", encoding="UTF-8") as f:
        return json.load(f)["dataset"]


def get_ner(model):
    if "ner" not in model.pipe_names:
        model.add_pipe("ner")
    return model.get_pipe("ner")


def add_training_labels(ner, train_data):
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    return ner


def disable_pips(model):
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in model.pipe_names if pipe not in pipe_exceptions]
    return unaffected_pipes


def get_batches(train_data):
    max_batch_size = 16
    if len(train_data) < 1000:
        max_batch_size /= 2
    if len(train_data) < 500:
        max_batch_size /= 2
    batch_size = compounding(1, max_batch_size, 1.001)
    return minibatch(train_data, size=batch_size)


def check_selection(section, given):
    if section not in given:
        log("error", "Incorrect option. Please, Try again.")
        return False
    return True


def count_accuracy(test, model, mode):
    all_answers = len(test)
    right_answers = 0

    all_tokens = len(test)
    right_tokens = 0

    total_answers = len(test)
    right_total = 0

    start_time = time.time()

    for entity in test:
        test_string, test_params, test_answer, test_tokens = get_entity_params(entity)
        entities = get_entities(model, test_string)

        for ent in entities:
            if len(entities) != 1:
                break
            elif test_answer == ent.text:
                right_answers += 1
                if ent.label_ == test_tokens:
                    right_tokens += 1
                    right_total += 1
                    if mode == "all":
                        log("good", "For {} predicted: {}".format(test_answer, ent.label_))
                else:
                    log("bad", "For <{}> expected: <{}>, predicted: <{}>".format(test_answer, test_tokens, ent.label_))
            else:
                if ent.label_ == test_tokens:
                    log("bad", "Right label <{}>, but Expected: <{}>, predicted: <{}>".format(ent.label_, test_answer,
                                                                                              ent.text))
                    right_tokens += 1
                else:
                    log("bad",
                        "For <{}> expected: <{}>, predicted: <{}> <{}>".format(test_answer, test_tokens, ent.text,
                                                                               ent.label_))

    result_time = time.time() - start_time

    return right_answers, right_tokens, right_total, all_answers, all_tokens, total_answers, result_time


def accuracy_checker(test, model, mode="false"):
    right_answers, right_tokens, right_total, all_answers, all_tokens, total_answers, result_time = \
        count_accuracy(test, model, mode)

    accuracy_entity = right_answers / all_answers * 100
    accuracy_type = right_tokens / all_tokens * 100
    accuracy_total = right_total / total_answers * 100

    print("\n")

    log("info", "Accuracy (entity recognition) is {:.2f}%".format(accuracy_entity))
    log("info", "Accuracy (type recognition) is {:.2f}%".format(accuracy_type))
    log("info", "Accuracy (total) is {:.2f}%".format(accuracy_total))
    log("info", "Time: {:.2f}s".format(result_time))


def train_model(model, unaffected_pipes, train_data, state):
    iterations = 5

    train_entities = []
    for texts, annotations in train_data:
        train_entities.append(Example.from_dict(model.make_doc(texts), annotations))

    if state == "new":
        optimizer = model.initialize(lambda: train_entities)
    elif state == "continue":
        optimizer = model.resume_training()
    else:
        optimizer = None

    for i in range(iterations):
        log("info", f"Training... {i + 1}/{iterations}")

        random.shuffle(train_entities)
        batches = get_batches(train_entities)

        for batch in batches:
            model.update(batch, sgd=optimizer)
    return model


def get_entities(model, test_data):
    doc = model(test_data)
    return doc.ents


def set_meta_info(model, name, version):
    model.meta["name"] = name
    model.meta["version"] = version
    return model


def predict_sample(model, inputed_data):
    entities = get_entities(model, inputed_data)

    log("info", "Results:")
    for ent in entities:
        log("ask", "{} ===> {}".format(ent.label_, ent.text))


def test_sample_model(model, test_data):
    entities = get_entities(model, test_data)
    print("Data for test:", test_data)
    print("Entities", [(ent.text, ent.label_) for ent in entities])


def save_model(model, models_dir):
    models_dir = Path(models_dir)

    if not models_dir.exists():
        models_dir.mkdir()

    model.to_disk(models_dir)


def get_entity_params(entity):
    test_string = entity[0]
    test_params = entity[1]["entities"][0]
    test_answer = test_string[test_params[0]:test_params[1]]
    test_tokens = test_params[2]
    return test_string, test_params, test_answer, test_tokens


def train_pipeline(dataset_filename, model_folder):
    model = create_model()

    log("info", f"Loading test dataset... ({dataset_filename})")
    train_data = load_train_dataset(dataset_filename)

    log("info", "Adding custom labels...")
    ner = get_ner(model)
    ner = add_training_labels(ner, train_data)

    model_pips = disable_pips(model)

    log("info", "Training model...")
    trained_model = train_model(model, model_pips, train_data, "new")

    log("info", f"Saving model as {model_folder} directory...")
    save_model(trained_model, model_folder)
    log("info", "Model saved!")


def continue_train_pipeline(model_dir, dataset_filename, model_folder):
    model = load_model(model_dir)

    log("info", f"Loading test dataset... ({dataset_filename})")
    train_data = load_train_dataset(dataset_filename)

    log("info", "Adding custom labels...")
    ner = get_ner(model)
    ner = add_training_labels(ner, train_data)

    model_pips = disable_pips(model)

    log("info", "Training model...")
    trained_model = train_model(model, model_pips, train_data, "continue")

    log("info", f"Saving model as {model_folder} directory")
    save_model(trained_model, model_folder)
    log("info", "Model saved!")


def test_auto_pipeline(model_dir, dataset_filename, logs_mode):
    model = load_model(model_dir)

    test_data = load_train_dataset(dataset_filename)

    print()
    accuracy_checker(test_data, model, logs_mode)
    print()


def file_handling(model_dir, filename, mode):
    file_data = txt_parsing(filename)
    temp_data = file_data.copy()

    model = load_model(model_dir)

    for entity in file_data:
        found_data = get_entities(model, entity)
        temp = entity
        if found_data:
            for obj in found_data:
                if mode == "replace":
                    generated = generate_random(obj.label_)
                    if generated:
                        temp = temp.replace(obj.text, generated)
                elif mode == "hide":
                    hidden = list(temp)
                    hidden_length = len(hidden)
                    if hidden_length >= 4:
                        hidden = ("***"
                                  + temp[int(hidden_length / 2):]
                                  + "***")
                    temp = temp.replace(obj.text, hidden)
        temp_data[file_data.index(entity)] = temp

    with open("result.txt", "w", encoding="UTF-8") as f:
        f.writelines("\n".join(temp_data))
