from tkinter import Tk
from tkinter.filedialog import askopenfilename

from src.enumeration.main_menu import MainMenu
from src.enumeration.bank import Bank
from src.factory.statement_factory import StatementFactory
from src.exception.app_exceptions import CsvFileNotSelected, MainMenuInputOutOfRange
from src.spending_category import SpendingCategoryOutOfRange, SpendingCategoryValueNotFound


def main_application():
    print_introduction()
    while True:
        try:
            main_option = get_input_from_main_menu()
            if main_option == MainMenu.OPEN_CHASE_CSV_FILE.value:
                path_to_csv_file = get_path_to_csv_file_from_user()
                statement = StatementFactory.make_statement(Bank.CHASE, path_to_csv_file)
            elif main_option == MainMenu.OPEN_CITI_CSV_FILE.value:
                path_to_csv_file = get_path_to_csv_file_from_user()
                statement = StatementFactory.make_statement(Bank.CITI, path_to_csv_file)
            elif main_option == MainMenu.EXIT.value:
                break

            month = int(input('\nWhich month would you like to analyze? : (ex. 5) '))
            year = int(input('Enter year: (ex 2018) '))
            transactions = statement.get_spendings_for_the_month(month, year)
            statement.categorize_each_transaction(transactions)
            spending_report = statement.get_sum_of_spending_in_each_category(transactions)

            print('\n SUMMARY: ')
            print(spending_report)

        except CsvFileNotSelected:
            pass
        except (ValueError, MainMenuInputOutOfRange, SpendingCategoryOutOfRange, SpendingCategoryValueNotFound):
            print('\n ERROR: Invalid option')


def print_introduction():
    print(
"""
**************************
Spending Tracker v1.0 Beta
**************************
Track your spending,
Adjust your spending,
And get rich!
-------------------------
Created by Brian Choi
**************************

""")


def get_input_from_main_menu():
    print(
""""
Please choose one from the following options:

1) Open a Chase Bank statement in csv file
2) Open a Citi Bank statement in csv file
3) Exit

""")
    user_input = int(input('Enter (ex. 1): '))
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
