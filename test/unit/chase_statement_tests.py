from unittest.mock import patch

import pytest
import csv

from src.chase_statement import ChaseStatement, KEY_TRANSACTION_DATE, KEY_AMOUNT


@pytest.fixture
@patch('src.statement.Statement._read_rows_from_csv_file', lambda *args, **kwargs: None)
@patch('src.chase_statement.ChaseStatement._sort_rows_by', lambda *args, **kwargs: None)
def chase_statement():
    chase_statement = ChaseStatement(path_to_csv_file='_')
    from collections import OrderedDict
    chase_statement.rows = [OrderedDict([('Type', 'Sale'),
                                        ('Trans Date', '01/01/2017'),
                                        ('Post Date', '01/02/2017'),
                                        ('Description', 'description 1'),
                                        ('Amount', '-01.01')]),
                            OrderedDict([('Type', 'Sale'),
                                         ('Trans Date', '01/02/2017'),
                                         ('Post Date', '01/02/2017'),
                                         ('Description', 'description 2'),
                                         ('Amount', '-01.02')]),
                            OrderedDict([('Type', 'Sale'),
                                         ('Trans Date', '01/03/2017'),
                                         ('Post Date', '01/04/2017'),
                                         ('Description', 'description 3'),
                                         ('Amount', '-01.03')]),
                            OrderedDict([('Type', 'Sale'),
                                         ('Trans Date', '01/04/2017'),
                                         ('Post Date', '01/06/2017'),
                                         ('Description', 'description 4'),
                                         ('Amount', '-01.04')]),
                            OrderedDict([('Type', 'Sale'),
                                         ('Trans Date', '01/05/2017'),
                                         ('Post Date', '01/06/2017'),
                                         ('Description', 'description 5'),
                                         ('Amount', '-01.05')]),
                            OrderedDict([('Type', 'Sale'),
                                         ('Trans Date', '01/06/2017'),
                                         ('Post Date', '01/06/2017'),
                                         ('Description', 'description 6'),
                                         ('Amount', '-01.06')])
                            ]
    return chase_statement


def test_dates_between_01_02_2017_to_01_04_2017_returns_3_rows(chase_statement):
    rows = chase_statement._filter_rows_by_date(start_date_str_inclusive='01/02/2017',
                                                end_date_str_inclusive='01/04/2017')
    assert 3, len(rows)


def test_dates_out_of_range_returns_0_rows(chase_statement):
    rows = chase_statement._filter_rows_by_date(start_date_str_inclusive='02/01/2017',
                                                end_date_str_inclusive='02/02/2017')
    assert 0 == len(rows)


def test_same_start_date_and_end_date_returns_1_row(chase_statement):
    rows = chase_statement._filter_rows_by_date(start_date_str_inclusive='01/01/2017',
                                                end_date_str_inclusive='01/01/2017')
    assert 1 == len(rows)


def test_range_from_2015_to_2020_returns_6_rows(chase_statement):
    rows = chase_statement._filter_rows_by_date(start_date_str_inclusive='01/01/2015',
                                                end_date_str_inclusive='12/31/2020')
    assert 6 == len(rows)


def test_january_returns_6_rows(chase_statement):
    rows = chase_statement.get_rows_for_the_month(month='1', year='2017')
    assert 6 == len(rows)


# class ChaseStatementTests(unittest.TestCase):
#     def setUp(self):
#         raw_data = {'Type': ['Sale', 'Sale', 'Sale', 'Sale', 'Sale', 'Sale',],
#                     'Trans Date': ['01/01/2017', '01/02/2017', '01/03/2017', '01/04/2017', '01/05/2017', '01/06/2017'],
#                     'Post Date': ['02/01/2017', '02/02/2017', '02/03/2017', '02/04/2017', '02/05/2017', '02/06/2017'],
#                     'Description:': ['Desc1', 'Desc2', 'Desc3', 'Desc4', 'Desc5', 'Desc6'],
#                     'Amount': ['-1.00', '-2.00', '-3.00', '-4.00', '-5.00', '6.00']}
#         data_frame = pandas.DataFrame(raw_data, columns=['Type', 'Trans Date', 'Post Date', 'Description', 'Amount'])
#         self.chase_statement = self._get_chase_statement()
#         self.chase_statement.rows = data_frame
#         self.chase_statement.rows[KEY_AMOUNT] = self.chase_statement.rows[KEY_AMOUNT].astype(float).fillna(0.0)
#
#     @patch('src.chase_statement.ChaseStatement.__init__', lambda *args, **kwargs: None)
#     def _get_chase_statement(self):
#         return ChaseStatement('_')
#
#     def test_dafaframe_query_with_dates_between_01_02_2017_to_01_04_2017_returns_3_rows(self):
#         rows = self.chase_statement._get_rows_from_start_date_inclusive_to_end_date_inclusive('01/02/2017',
#                                                                                                  '01/04/2017')
#         self.assertEqual(3, len(rows))
#
#         valid_dates = ['01/02/2017', '01/03/2017', '01/04/2017']
#         for row in rows[KEY_TRANSACTION_DATE]:
#             self.assertTrue(row in valid_dates)
#
#     def test_dafaframe_query_with_dates_out_of_range_returns_no_rows(self):
#         rows = self.chase_statement._get_rows_from_start_date_inclusive_to_end_date_inclusive('05/02/2017',
#                                                                                                  '05/04/2017')
#         self.assertEqual(0, len(rows))
#
#     def test_dafaframe_query_with_dates_between_minimum_and_above_maximum_available_returns_5_rows(self):
#         rows = self.chase_statement._get_rows_from_start_date_inclusive_to_end_date_inclusive('01/01/2017',
#                                                                                                  '12/31/2099')
#         self.assertEqual(5, len(rows))
#
#     def test_dafaframe_query_with_dates_between_below_minimum_and_above_maximum_available_returns_5_rows(self):
#         rows = self.chase_statement._get_rows_from_start_date_inclusive_to_end_date_inclusive('01/01/1990',
#                                                                                                  '12/31/2099')
#         self.assertEqual(5, len(rows))
#
#     def test_get_dataframe_for_january_2017_return_5_rows(self):
#         rows = self.chase_statement.get_rows_for_the_month('1', '2017')
#         self.assertEqual(5, len(rows))
#
#     def test_get_dataframe_for_february_2017_return_0_rows(self):
#         rows = self.chase_statement.get_rows_for_the_month('2', '2017')
#         self.assertEqual(0, len(rows))
