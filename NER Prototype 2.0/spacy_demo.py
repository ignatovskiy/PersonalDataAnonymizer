import random
from pathlib import Path

import json
import spacy
from spacy.util import minibatch, compounding

			
def run_pipeline():
	test_data = "220 Lenin Ave, Flat 98 600434"

	model = load_model()

	print("Enter dataset filename:")
	dataset_filename = input()

	train_data = load_train_dataset(dataset_filename)

	ner = get_ner(model)
	ner = add_training_labels(ner, train_data)

	model_optimizer = model.begin_training()

	model_pips = disable_pips(model)
	trained_model = train_model(model, model_pips, train_data, model_optimizer)

	print("Enter directory for model")
	model_folder = input()

	save_model(trained_model, model_folder)
	test_model(trained_model, test_data)


def load_model():
	print("Creating model...")
	return spacy.blank("en")


def load_train_dataset(dataset_name):
	print("Loading train dataset...")
	with open(dataset_name, "r", encoding="UTF-8") as f:
		dataset = json.load(f)["dataset"]
	return dataset


def get_ner(model):
	if "ner" not in model.pipe_names:
		ner = model.create_pipe("ner")
		model.add_pipe(ner)
	return model.get_pipe("ner")


def add_training_labels(ner, train_data):
	print("Adding training labels...")
	for _, annotations in train_data:
		for ent in annotations.get("entities"):
			ner.add_label(ent[2])
	return ner


def disable_pips(model):
	pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
	unaffected_pipes = [pipe for pipe in model.pipe_names if pipe not in pipe_exceptions]
	return unaffected_pipes


def get_batches(train_data, model_type):
    max_batch_size = 16
    if len(train_data) < 1000:
        max_batch_size /= 2
    if len(train_data) < 500:
        max_batch_size /= 2
    batch_size = compounding(1, max_batch_size, 1.001)
    return minibatch(train_data, size=batch_size)


def train_model(model, unaffected_pipes, train_data, model_optimizer):
	print("Training dataset...")
	iterations = 5
	with model.disable_pipes(*unaffected_pipes):
		for iteration in range(iterations):
			random.shuffle(train_data)
			losses = {}
			batches = get_batches(train_data, "ner")
			losses_sum = 0
			for batch in batches:
				texts, annotations = zip(*batch)
				model.update(texts,
							annotations,
							sgd=model_optimizer,
							drop=0.2,
							losses=losses)
				losses_sum += losses["ner"]
			print("Losses:", losses_sum / len(list(batches)))
			print("Epoch {}/{}".format(str(iteration + 1), str(iterations)))
	return model


def test_model(model, test_data):
	doc = model(test_data)
	print("Data for test:", test_data)
	print("Entities", [(ent.text, ent.label_) for ent in doc.ents])


def save_model(model, models_dir):
	models_dir = Path(models_dir)

	if not models_dir.exists():
		models_dir.mkdir()

	model.meta["name"] = "stable_model"
	model.to_disk(models_dir)


def main():
	run_pipeline()


if __name__ == "__main__":
	main()