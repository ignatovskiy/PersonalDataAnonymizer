import spacy
import os


def main():
	os.system('clear')
	print("Enter name of model's folder:")
	model_dir = input()
	model = spacy.load(model_dir)
	
	os.system('clear')
	print("Model was loaded!")

	while True:
		print("Input new string or text 'stop':")
		inputed_string = input()
		
		os.system('clear')
		if inputed_string == "stop":
			break

		doc = model(inputed_string)

		print("Results:")
		for ent in doc.ents:
			print(ent.label_, "===>", ent.text)



if __name__ == "__main__":
	main()