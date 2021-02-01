import spacy
import os


def main():
	inputed_string = ""
	model_dir = "models_dir"

	os.system('clear')
	while True:
		print("Input new string or text 'stop': \n")
		inputed_string = input()
		os.system('clear')
		if inputed_string == "stop":
			break

		model = spacy.load(model_dir)
		doc = model(inputed_string)

		print("Results:")
		for ent in doc.ents:
			print(ent.label_, "===>", ent.text)



if __name__ == "__main__":
	main()