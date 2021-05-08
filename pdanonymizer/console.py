import argparse

from pdanonymizer import dataset_converter, dataset_creator
from pdanonymizer.utils import *


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="-a train -d [dataset file] -o [model dir]\n"
                                                 "-a post_train -m [model dir] -d [dataset file] -o ["
                                                 "model folder]\n"
                                                 "-a test_auto -m [model dir] -d [dataset file]\n"
                                                 "-a test_manual -m [model dir] -d [string]\n"
                                                 "-a convert -d [dataset file]\n"
                                                 "-a create -d [raw dataset file] -v [entities amount] -o"
                                                 "[dataset file]\n"
                                                 "-a predict_file -m [model dir] -d [file] -o [file]\n"
                                                 "-a mask_file -m [model dir] -d [file] -o [file]\n"
                                                 "-a mask_image -d [input image filename] -o [output image filename]\n"
                                                 "-a interact\n")

    parser.add_argument('-a', '--action', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-m', '--model', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-d', '--data', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-l', '--logs', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-o', '--output', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-v', '--value', type=int, help=argparse.SUPPRESS)

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
            if args.data and args.model and args.output:
                file_handling(args.model, args.data, args.output, "replace")
            else:
                log("error", "Error. Set --model, --data and --output parameters.")
        elif action == "mask_file":
            if args.data and args.model and args.output:
                file_handling(args.model, args.data, args.output, "hide")
            else:
                log("error", "Error. Set --model, --data and --output parameters.")
        elif action == "mask_image":
            if args.data and args.output:
                image_handling_pipeline(args.data, args.output)
            else:
                log("error", "Error. Set --data and --output parameters.")
        elif action == "interact":
            menu_pipeline()
    else:
        io_handling()


if __name__ == "__main__":
    main()
