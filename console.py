from symbols import *
from utils import *


def show_test():
	os.system('clear')
	print(test_symbol)

def show_train():
	os.system('clear')
	print(train_symbol)


def handling_test_results_menu():
	selected_section = input("[ ]: ")

	if not check_selection(selected_section, ("9", "0")):
		handling_test_results_menu()
	elif selected_section == "0":
		return
	elif selected_section == "9":
		main()


def handling_train_results_menu():
	selected_section = input("[ ]: ")

	if not check_selection(selected_section, ("1", "2", "9", "0")):
		handling_train_results_menu()
	elif selected_section == "0":
		return
	elif selected_section == "1":
		show_test()
		handling_test_auto()
	elif selected_section == "2":
		show_test()
		handling_test_manual()
	elif selected_section == "9":
		main()


def handling_main_menu():
	selected_section = input("[ ]: ")

	if not check_selection(selected_section, ("1", "2", "0")):
		handling_main_menu()
	elif selected_section == "0":
		return
	elif selected_section == "1":
		show_train_menu()
		handling_train_menu()
	elif selected_section == "2":
		show_test_menu()
		handling_test_menu()


def handling_train_menu():
	selected_section = input("[ ]: ")

	if not check_selection(selected_section, ("1", "2", "9", "0")):
		handling_train_menu()
	elif selected_section == "0":
		return
	elif selected_section == "1":
		show_train()
		handling_train_start()
	elif selected_section == "2":
		show_train()
		handling_train_continue()
	elif selected_section == "9":
		main()

def handling_test_menu():
	selected_section = input("[ ]: ")

	if not check_selection(selected_section, ("1", "2", "9", "0")):
		handling_test_menu()
	elif selected_section == "0":
		return
	elif selected_section == "1":
		show_test()
		handling_test_auto()
	elif selected_section == "2":
		show_test()
		handling_test_manual()
	elif selected_section == "9":
		main()


def handling_train_start():
	model = create_model()

	log("ask", "Enter train dataset filename:")
	dataset_filename = input("[ ]: ")

	log("ask", "Enter directory for saving model:")
	model_folder = input("[ ]: ")
	print()

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

	print(train_result_menu)
	handling_train_results_menu()


def handling_train_continue():
	log("ask", "Enter model directory name:")
	model_dir = input("[ ]: ")
	model = load_model(model_dir)

	log("ask", "Enter train dataset filename:")
	dataset_filename = input("[ ]: ")

	log("ask", "Enter directory for saving model:")
	model_folder = input("[ ]: ")
	print()

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

	print(train_result_menu)
	handling_train_results_menu()


def handling_test_auto():
	log("ask", "Enter model directory name:")
	model_dir = input("[ ]: ")
	model = load_model(model_dir)

	log("ask", "Enter test dataset filename:")
	dataset_filename = input("[ ]: ")
	test_data = load_train_dataset(dataset_filename)

	log("ask", "Choose logs mode ('false' - only false recognitions, 'all' - all logs):")
	logs_mode = input("[ ]: ")

	print()
	accuracy_checker(test_data, model, logs_mode)
	print()

	print(test_result_menu)
	handling_test_results_menu()


def handling_test_manual():
	log("ask", "Enter model directory name:")
	model_dir = input("[ ]: ")
	model = load_model(model_dir)

	print()
	print(test_rtc)

	while True:
		inputed_string = input("[ ]: ")
		
		if inputed_string == "0":
			break	
		elif inputed_string == "9":
			main()
		else:
			predict_sample(model, inputed_string)


def show_main_menu():
	os.system('clear')
	print(start_symbol)
	print(main_menu)


def show_train_menu():
	show_train()
	print(train_menu)


def show_test_menu():
	show_test()
	print(test_menu)


def main():
	show_main_menu()
	handling_main_menu()


if __name__ == "__main__":
	main()