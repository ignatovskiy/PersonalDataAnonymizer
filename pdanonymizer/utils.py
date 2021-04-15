from pdanonymizer.symbols import *
from pdanonymizer.pipelines import *


def menu_pipeline():
    show_main_menu()
    handling_main_menu()


def handling_test_results_menu():
    selected_section = input("[ ]: ")

    if not check_selection(selected_section, ("9", "0")):
        handling_test_results_menu()
    elif selected_section == "0":
        return
    elif selected_section == "9":
        menu_pipeline()


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
        menu_pipeline()


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
        menu_pipeline()


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
        menu_pipeline()


def handling_train_start():
    log("ask", "Enter train dataset filename:")
    dataset_filename = input("[ ]: ")

    log("ask", "Enter directory for saving model:")
    model_folder = input("[ ]: ")
    print()

    train_pipeline(dataset_filename, model_folder)

    print(train_result_menu)
    handling_train_results_menu()


def handling_train_continue():
    log("ask", "Enter model directory name:")
    model_dir = input("[ ]: ")

    log("ask", "Enter train dataset filename:")
    dataset_filename = input("[ ]: ")

    log("ask", "Enter directory for saving model:")
    model_folder = input("[ ]: ")
    print()

    continue_train_pipeline(model_dir, dataset_filename, model_folder)

    print(train_result_menu)
    handling_train_results_menu()


def handling_test_auto():
    log("ask", "Enter model directory name:")
    model_dir = input("[ ]: ")

    log("ask", "Enter test dataset filename:")
    dataset_filename = input("[ ]: ")

    log("ask", "Choose logs mode ('false' - only false recognitions, 'all' - all logs):")
    logs_mode = input("[ ]: ")

    test_auto_pipeline(model_dir, dataset_filename, logs_mode)

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
            menu_pipeline()
        else:
            predict_sample(model, inputed_string)
