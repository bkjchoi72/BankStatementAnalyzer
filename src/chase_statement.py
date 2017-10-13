import calendar

from src.statement import Statement
from datetime import datetime, timedelta
from src.spending_category import SpendingCategory

KEY_TRANSACTION_DATE = 'Trans Date'
KEY_DESCRIPTION = 'Description'
KEY_AMOUNT = 'Amount'


class ChaseStatement(Statement):
    def __init__(self, path_to_csv_file):
        super(ChaseStatement, self).__init__(path_to_csv_file)
        self.loaded_csv[KEY_AMOUNT] = self.loaded_csv[KEY_AMOUNT].astype(float).fillna(0.0)

    @staticmethod
    def categorize_each_row_in_dataframe(rows):
        row_tuples = []
        spending_category = SpendingCategory()
        for i, row in rows.iterrows():
            chosen_category = spending_category.categorize_row_by_description(row[KEY_DESCRIPTION],
                                                                              row[KEY_TRANSACTION_DATE])
            row_tuples.append((row, chosen_category))

        return row_tuples

    def get_rows_for_the_month(self, month, year):
        weekday_of_first_day, number_of_days = calendar.monthrange(int(year), int(month))
        start_date_str = '{}/1/{}'.format(month, year)
        end_date_str = '{}/{}/{}'.format(month, number_of_days, year)

        return self._get_rows_between_start_date_inclusive_and_end_date_inclusive(start_date_str, end_date_str)

    @staticmethod
    def get_sum_of_spending_in_each_category(row_spending_tuples):
        spending_summary = {}
        for row, spending in row_spending_tuples:
            if spending_summary.get(spending.name, None):
                spending_summary[spending.name] += round(row[KEY_AMOUNT], 2)
            else:
                spending_summary[spending.name] = round(row[KEY_AMOUNT], 2)

        return spending_summary

    def _get_rows_between_start_date_inclusive_and_end_date_inclusive(self, start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
        number_of_days = (end_date - start_date).days
        valid_dates = [(start_date + timedelta(days=x)).strftime('%m/%d/%Y') for x in range(number_of_days + 1)]

        date_filter = self.loaded_csv[KEY_TRANSACTION_DATE].isin(valid_dates)
        spending_filter = self.loaded_csv[KEY_AMOUNT] < 0

        return self.loaded_csv[date_filter & spending_filter].sort_values(KEY_TRANSACTION_DATE)
