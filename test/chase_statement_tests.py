import unittest
import pandas
from mock import patch

from src.chase_statement import ChaseStatement, KEY_TRANSACTION_DATE, KEY_AMOUNT


class ChaseStatementTests(unittest.TestCase):
    def setUp(self):
        raw_data = {'Type': ['Sale', 'Sale', 'Sale', 'Sale', 'Sale', 'Sale',],
                    'Trans Date': ['01/01/2017', '01/02/2017', '01/03/2017', '01/04/2017', '01/05/2017', '01/06/2017'],
                    'Post Date': ['02/01/2017', '02/02/2017', '02/03/2017', '02/04/2017', '02/05/2017', '02/06/2017'],
                    'Description:': ['Desc1', 'Desc2', 'Desc3', 'Desc4', 'Desc5', 'Desc6'],
                    'Amount': ['-1.00', '-2.00', '-3.00', '-4.00', '-5.00', '6.00']}
        data_frame = pandas.DataFrame(raw_data, columns=['Type', 'Trans Date', 'Post Date', 'Description', 'Amount'])
        self.chase_statement = self._get_chase_statement()
        self.chase_statement.loaded_csv = data_frame
        self.chase_statement.loaded_csv[KEY_AMOUNT] = self.chase_statement.loaded_csv[KEY_AMOUNT].astype(float).fillna(0.0)

    @patch('src.chase_statement.ChaseStatement.__init__', lambda *args, **kwargs: None)
    def _get_chase_statement(self):
        return ChaseStatement('_')

    def test_dafaframe_query_with_dates_between_01_02_2017_to_01_04_2017_returns_3_rows(self):
        rows = self.chase_statement._get_rows_between_start_date_inclusive_and_end_date_inclusive('01/02/2017',
                                                                                                 '01/04/2017')
        self.assertEqual(3, len(rows))

        valid_dates = ['01/02/2017', '01/03/2017', '01/04/2017']
        for row in rows[KEY_TRANSACTION_DATE]:
            self.assertTrue(row in valid_dates)

    def test_dafaframe_query_with_dates_out_of_range_returns_no_rows(self):
        rows = self.chase_statement._get_rows_between_start_date_inclusive_and_end_date_inclusive('05/02/2017',
                                                                                                 '05/04/2017')
        self.assertEqual(0, len(rows))

    def test_dafaframe_query_with_dates_between_minimum_and_above_maximum_available_returns_5_rows(self):
        rows = self.chase_statement._get_rows_between_start_date_inclusive_and_end_date_inclusive('01/01/2017',
                                                                                                 '12/31/2099')
        self.assertEqual(5, len(rows))

    def test_dafaframe_query_with_dates_between_below_minimum_and_above_maximum_available_returns_5_rows(self):
        rows = self.chase_statement._get_rows_between_start_date_inclusive_and_end_date_inclusive('01/01/1990',
                                                                                                 '12/31/2099')
        self.assertEqual(5, len(rows))

    def test_get_dataframe_for_january_2017_return_5_rows(self):
        rows = self.chase_statement.get_rows_for_the_month('1', '2017')
        self.assertEqual(5, len(rows))

    def test_get_dataframe_for_february_2017_return_0_rows(self):
        rows = self.chase_statement.get_rows_for_the_month('2', '2017')
        self.assertEqual(0, len(rows))
