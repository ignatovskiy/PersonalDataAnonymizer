import json
import spacy
import time


def load_dataset(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return json.load(f)["dataset"]


def main():
    print("Enter model dir")
    model_dir = input()
    print("Enter test dataset filename:")
    test_file = input()

    start_time = time.time()
    print("Loading model...")
    model = spacy.load(model_dir)
    print("Loading test dataset...")
    test = load_dataset(test_file)

    all_answers = len(test)
    right_answers = 0

    all_tokens = len(test)
    right_tokens = 0

    total_answers = len(test)
    right_total = 0 

    for entity in test:
        test_string = entity[0]
        test_params = entity[1]["entities"][0]
        test_answer = test_string[test_params[0]:test_params[1]]
        test_tokens = test_params[2]
        doc = model(test_string)

        for ent in doc.ents:
            if len(doc.ents) != 1:
                break
            elif test_answer == ent.text:
                right_answers += 1
                if ent.label_ == test_tokens:
                    right_tokens += 1
                    right_total += 1
                else:
                    print("For {} expected: {}, predicted: {}".format(test_answer, test_tokens, ent.label_))
            else:
                print("Expected: {}, predicted: {}".format(test_answer, ent.text))
                if ent.label_ == test_tokens:
                    right_tokens += 1
                else:
                    print("For {} expected: {}, predicted: {} {}".format(test_answer, test_tokens, ent.text, ent.label_))

    result_time = time.time() - start_time

    print("\nAccuracy (entity recognition) is {}%".format(right_answers / all_answers * 100))
    print("Accuracy (type recognition) is {}%".format(right_tokens / all_tokens * 100))
    print("Accuracy (total) is {}%".format(right_total / total_answers * 100))
    print("Time: {} s".format(result_time))


if __name__ == "__main__":
    main()
