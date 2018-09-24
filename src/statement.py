import csv
from abc import abstractmethod, ABC

from src.transaction import Transaction


class Statement(ABC):
    KEY_TRANSACTION_DATE = ''
    KEY_DESCRIPTION = ''
    KEY_AMOUNT = ''

    def __init__(self, path_to_csv_file):
        self.transactions = self._read_transactions_from_csv_file(path_to_csv_file)

    @abstractmethod
    def get_spendings_for_the_month(self, month, year):
        pass

    @staticmethod
    @abstractmethod
    def categorize_each_transaction(rows):
        pass

    @staticmethod
    @abstractmethod
    def get_sum_of_spending_in_each_category(row_spending_tuples):
        pass

    def _read_transactions_from_csv_file(self, path_to_csv_file):
        transactions = []
        with open(path_to_csv_file) as fin:
            csv_reader = csv.DictReader(fin)
            for row in csv_reader:
                transactions.append(
                    Transaction(date=row[self.KEY_TRANSACTION_DATE], description=row[self.KEY_DESCRIPTION],
                                amount=float(row[self.KEY_AMOUNT])))

            return transactions
