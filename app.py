from statement import Statement
from Tkinter import Tk
from tkFileDialog import askopenfilename
from main_menu import MainMenu


def main_application():
    print_introduction()
    main_option = get_input_from_main_menu()
    while main_option != MainMenu.EXIT:
        if main_option == MainMenu.OPEN_CHASE_CSV_FILE:
            path_to_csv_file = get_path_to_csv_file_from_user()
            if path_to_csv_file:
                statement = Statement(path_to_csv_file)
                statement.get_first_5_rows_of_csv()
        elif main_option == MainMenu.OPEN_CITI_CSV_FILE:
            pass

        main_option = get_input_from_main_menu()


def print_introduction():
    print '\n**************************'
    print 'Spending Tracker v1.0 Beta'
    print '**************************'
    print 'Track your spending,'
    print 'Adjust your spending,'
    print 'And get rich!'
    print '--------------------------'
    print 'Created by Brian Choi'
    print '**************************\n'


def get_input_from_main_menu():
    print '\nPlease choose one from the following options:'
    print '1) Open a Chase Bank statement in csv file'
    print '2) Open a Citi Bank statement in csv file'
    print '3) Exit'
    print ''
    user_input = raw_input('Enter (ex. 1): ')
    return int(user_input)


def get_path_to_csv_file_from_user():
    Tk().withdraw()
    path_to_file = askopenfilename()
    return path_to_file


if __name__ == '__main__':
    main_application()
