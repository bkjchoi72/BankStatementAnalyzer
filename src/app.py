from Tkinter import Tk
from tkFileDialog import askopenfilename

from src.enumeration.main_menu import MainMenu
from src.enumeration.bank import Bank
from src.factory.statement_factory import StatementFactory
from src.exception.app_exceptions import CsvFileNotSelected, MainMenuInputOutOfRange


def main_application():
    print_introduction()
    main_option = get_input_from_main_menu()
    while main_option != MainMenu.EXIT:
        try:
            if main_option == MainMenu.OPEN_CHASE_CSV_FILE:
                path_to_csv_file = get_path_to_csv_file_from_user()
                statement = StatementFactory.make_statement(Bank.CHASE, path_to_csv_file)
                first_five_rows = statement.get_first_5_rows_of_csv()
                for index, row in first_five_rows.iterrows():
                    for column in row:
                        print column
                print first_five_rows
            elif main_option == MainMenu.OPEN_CITI_CSV_FILE:
                path_to_csv_file = get_path_to_csv_file_from_user()
                statement = StatementFactory.make_statement(Bank.CITI, path_to_csv_file)
        except CsvFileNotSelected:
            pass
        except (ValueError, MainMenuInputOutOfRange):
            print 'Please choose a valid option'

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
    user_input = int(raw_input('Enter (ex. 1): '))
    number_of_available_options = [option for option in MainMenu]
    if user_input < 1 or user_input > len(number_of_available_options):
        raise MainMenuInputOutOfRange

    return user_input


def get_path_to_csv_file_from_user():
    Tk().withdraw()
    path_to_file = askopenfilename()
    if not path_to_file:
        raise CsvFileNotSelected

    return path_to_file


if __name__ == '__main__':
    main_application()
