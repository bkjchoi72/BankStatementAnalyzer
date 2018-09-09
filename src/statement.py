import csv
from abc import abstractmethod, ABC


class Statement(ABC):
    def __init__(self, path_to_csv_file):
        self.rows = self._read_rows_from_csv_file(path_to_csv_file)

    @abstractmethod
    def get_rows_for_the_month(self, month, year):
        pass

    @staticmethod
    @abstractmethod
    def categorize_each_row(rows):
        pass

    @staticmethod
    @abstractmethod
    def get_sum_of_spending_in_each_category(row_spending_tuples):
        pass

    def _read_rows_from_csv_file(self, path_to_csv_file):
        with open(path_to_csv_file) as fin:
            csv_reader = csv.DictReader(fin)
            return [row for row in csv_reader]
