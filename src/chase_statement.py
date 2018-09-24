import calendar

from src.statement import Statement
from datetime import datetime, timedelta
from src.spending_category import SpendingCategory


class ChaseStatement(Statement):
    KEY_TRANSACTION_DATE = 'Trans Date'
    KEY_DESCRIPTION = 'Description'
    KEY_AMOUNT = 'Amount'

    def __init__(self, path_to_csv_file):
        super(ChaseStatement, self).__init__(path_to_csv_file)
        self._sort_transactions_by_ascending_date()

    @staticmethod
    def categorize_each_transaction(transactions):
        spending_category = SpendingCategory()
        for transaction in transactions:
            chosen_category = spending_category.categorize_transaction_by_description(transaction.amount,
                                                                                      transaction.date,
                                                                                      transaction.description)
            transaction.category = chosen_category

        return transactions

    def get_spendings_for_the_month(self, month, year):
        weekday_of_first_day, number_of_days = calendar.monthrange(int(year), int(month))
        start_date_str = '{}/1/{}'.format(month, year)
        end_date_str = '{}/{}/{}'.format(month, number_of_days, year)

        filtered_transactions = self._filter_transactions_by_date(self.transactions, start_date_str, end_date_str)
        return self._filter_transactions_by_amount(filtered_transactions, maximum_inclusive=0)

    @staticmethod
    def get_sum_of_spending_in_each_category(transactions):
        spending_summary = {}
        for transaction in transactions:
            if spending_summary.get(transaction.category.name, None):
                spending_summary[transaction.category.name] += round(transaction.amount, 2)
            else:
                spending_summary[transaction.category.name] = round(transaction.amount, 2)

        for category, amount in spending_summary.items():
            spending_summary[category] = f'{-amount:.2f}'
        return spending_summary

    def _filter_transactions_by_date(self, transactions, start_date_str_inclusive, end_date_str_inclusive):
        start_date = datetime.strptime(start_date_str_inclusive, '%m/%d/%Y')
        end_date = datetime.strptime(end_date_str_inclusive, '%m/%d/%Y')
        number_of_days = (end_date - start_date).days
        valid_dates = [(start_date + timedelta(days=x)).strftime('%m/%d/%Y') for x in range(number_of_days + 1)]

        filtered_transactions = []
        for transaction in transactions:
            if transaction.date in valid_dates:
                filtered_transactions.append(transaction)

        return filtered_transactions

    def _filter_transactions_by_amount(self, transactions, minimum_inclusive=float('-inf'),
                                       maximum_inclusive=float('inf')):
        filtered_transactions = []
        for transaction in transactions:
            if minimum_inclusive <= transaction.amount <= maximum_inclusive:
                filtered_transactions.append(transaction)

        return filtered_transactions

    def _sort_transactions_by_ascending_date(self):
        self.transactions = sorted(self.transactions, key=lambda transaction: transaction.date)
