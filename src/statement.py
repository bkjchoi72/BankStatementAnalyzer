import pandas
from abc import ABCMeta, abstractmethod


class Statement(object):
    __metaclass__ = ABCMeta

    def __init__(self, path_to_csv_file):
        self.loaded_csv = pandas.read_csv(path_to_csv_file)

    def get_first_5_rows_of_csv(self):
        return self.loaded_csv.head()

    @abstractmethod
    def get_rows_for_the_month(self, month, year):
        pass

    @staticmethod
    @abstractmethod
    def categorize_each_row_in_dataframe(rows):
        pass

    @staticmethod
    @abstractmethod
    def get_sum_of_spending_in_each_category(row_spending_tuples):
        pass
