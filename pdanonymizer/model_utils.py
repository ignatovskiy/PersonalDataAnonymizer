from pathlib import Path
import random
import sys
import time

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding

from pdanonymizer.parsers import *
from pdanonymizer.generators import generate_random
from pdanonymizer.images_handlers import *


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
    elif state in ("continue", "post"):
        optimizer = model.resume_training()
    else:
        optimizer = None

    for i in range(iterations):
        if state != "post":
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


def post_train(model_dir, entity):
    model = load_model(model_dir)

    ner = get_ner(model)
    ner = add_training_labels(ner, entity)

    model_pips = disable_pips(model)
    trained_model = train_model(model, model_pips, entity, "post")
    save_model(trained_model, model_dir)


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


def image_handling_pipeline(filename, output_filename):
    log("info", f"Loading {filename} image...")
    hide_data_image(filename, output_filename)
    log("info", f"Image was saved as {output_filename}!")


def test_auto_pipeline(model_dir, dataset_filename, logs_mode):
    model = load_model(model_dir)

    test_data = load_train_dataset(dataset_filename)

    print()
    accuracy_checker(test_data, model, logs_mode)
    print()


def hide_data(data, obj):
    hidden = list(data)
    hidden_length = int(len(hidden) / 2)
    hidden = (data[:hidden_length]
              + "*" * hidden_length)
    temp = data.replace(obj.text, hidden)
    return temp


def check_data(label, text):
    if label == "NAME" and len(text) > 3 and text.lower() != text:
        return True
    elif label == "PHONE" and len(text) >= 6:
        return True
    elif label == "BIRTHDAY" and 10 >= len(text) >= 8:
        return True
    elif label == "EMAIL" and "@" in text and "." in text:
        return True
    elif label == "ID" and len(text) >= 4:
        return True
    elif label == "ADDRESS" and len(text) >= 20:
        return True
    else:
        return False


def replace_data(data, obj, model_dir):
    if check_data(obj.label_, obj.text):
        generated = generate_random(obj.label_)
        if generated:
            temp = data.replace(obj.text, generated)
        else:
            temp = data
        return temp
    else:
        train_data = [[obj.text, {'entities': []}]]
        post_train(model_dir, train_data)
        return data


def web_handling(input_string, model_dir='models/model_10000'):
    model = load_model(model_dir)
    temp_string = input_string.copy()

    for inp_str in input_string:
        found_data = get_entities(model, inp_str)
        temp = inp_str
        if found_data:
            for obj in found_data:
                temp = replace_data(temp, obj, model_dir)
        temp_string[input_string.index(inp_str)] = temp
    return "\n".join(temp_string)


def io_handling(model_dir="models/model_10000"):
    model = load_model(model_dir)

    input_stream = sys.stdin.read().split("\n")
    temp_stream = input_stream.copy()

    for item in input_stream:
        found_data = get_entities(model, item)
        temp = item
        if found_data:
            for obj in found_data:
                temp = replace_data(temp, obj, model_dir)
        temp_stream[input_stream.index(item)] = temp

    sys.stdout.write("\n".join(temp_stream))


def file_handling(model_dir, filename, output, mode):
    file_extension = filename.split(".")[-1].lower()

    if file_extension == "csv":
        file_data = csv_parsing(filename)
    else:
        file_data = txt_parsing(filename)

    columns_titles = file_data[0]

    temp_data = file_data.copy()

    model = load_model(model_dir)

    for entity in file_data:
        found_data = get_entities(model, entity)
        temp = entity
        if found_data:
            for obj in found_data:
                if mode == "replace":
                    temp = replace_data(temp, obj, model_dir)
                elif mode == "hide":
                    temp = hide_data(temp, obj)
        temp_data[file_data.index(entity)] = temp

    with open(output, "w", encoding="UTF-8") as f:
        if file_extension == "csv":
            temp_data[0] = columns_titles
        output_data = "\n".join(temp_data)
        if file_extension == "csv":
            output_data = output_data.replace("_", ",")
        f.writelines(output_data)
