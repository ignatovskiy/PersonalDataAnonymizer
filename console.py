import argparse

import dataset_converter
import dataset_creator

from utils import *


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('--action', type=str)
	parser.add_argument('--model', type=str)
	parser.add_argument('--data', type=str)
	parser.add_argument('--logs', type=str)
	parser.add_argument('--output', type=str)
	parser.add_argument('--value', type=int)

	args = parser.parse_args()

	if args.action:
		action = args.action

		if action == "train":
			if args.data and args.output:
				train_pipeline(args.data, args.output)
			else:
				log("error", "Error. Set --data and --output parameters.")
		elif action == "post_train":
			if args.model and args.data and args.output:
				continue_train_pipeline(args.model, args.data, args.output)
			else:
				log("error", "Error. Set --data, --model and --output parameters.")
		elif action == "test_auto":
			if args.model and args.data and args.logs:
				test_auto_pipeline(args.model, args.data, args.logs)
			else:
				log("error", "Error. Set --data, --model and --logs parameters.")
		elif action == "test_manual":
			if args.model and args.data:
				model = load_model(args.model)
				predict_sample(model, args.data)
			else:
				log("error", "Error. Set --data and --model parameters.")
		elif action == "convert":
			if args.data:
				dataset_converter.main(args.data)
			else:
				log("error", "Error. Set --data parameter.")
		elif action == "create":
			if args.data and args.output and args.value:
				dataset_creator.create(args.value, args.output, args.data)
			else:
				log("error", "Error. Set --data, --value and --output parameters.")
		elif action == "predict_file":
			if args.data and args.model:
				file_handling(args.model, args.data)
			else:
				log("error", "Error. Set --model and --data parameters.")
	else:
		menu_pipeline()


if __name__ == "__main__":
	main()
