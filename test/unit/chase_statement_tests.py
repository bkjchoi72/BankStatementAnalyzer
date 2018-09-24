from unittest.mock import patch

import pytest

from src.chase_statement import ChaseStatement
from src.transaction import Transaction


@pytest.fixture
@patch('src.statement.Statement._read_transactions_from_csv_file', lambda *args, **kwargs: None)
@patch('src.chase_statement.ChaseStatement._sort_transactions_by_ascending_date', lambda *args, **kwargs: None)
def chase_statement():
    chase_statement = ChaseStatement(path_to_csv_file='_')
    chase_statement.transactions = [
        Transaction(date='01/01/2017', description='description 1', amount=-01.01),
        Transaction(date='01/02/2017', description='description 2', amount=-01.02),
        Transaction(date='01/03/2017', description='description 3', amount=-01.03),
        Transaction(date='01/04/2017', description='description 4', amount=-01.04),
        Transaction(date='01/05/2017', description='description 5', amount=-01.05),
        Transaction(date='01/06/2017', description='description 6', amount=-01.06)
    ]

    return chase_statement


def test_dates_between_01_02_2017_to_01_04_2017_returns_3_rows(chase_statement):
    transactions = chase_statement._filter_transactions_by_date(chase_statement.transactions,
                                                                start_date_str_inclusive='01/02/2017',
                                                                end_date_str_inclusive='01/04/2017')
    assert 3, len(transactions)


def test_dates_out_of_range_returns_0_rows(chase_statement):
    transactions = chase_statement._filter_transactions_by_date(chase_statement.transactions,
                                                                start_date_str_inclusive='02/01/2017',
                                                                end_date_str_inclusive='02/02/2017')
    assert 0 == len(transactions)


def test_same_start_date_and_end_date_returns_1_row(chase_statement):
    transactions = chase_statement._filter_transactions_by_date(chase_statement.transactions,
                                                                start_date_str_inclusive='01/01/2017',
                                                                end_date_str_inclusive='01/01/2017')
    assert 1 == len(transactions)


def test_range_from_2015_to_2020_returns_6_rows(chase_statement):
    transactions = chase_statement._filter_transactions_by_date(chase_statement.transactions,
                                                                start_date_str_inclusive='01/01/2015',
                                                                end_date_str_inclusive='12/31/2020')
    assert 6 == len(transactions)


def test_january_returns_6_rows(chase_statement):
    transactions = chase_statement.get_spendings_for_the_month(month='1', year='2017')
    assert 6 == len(transactions)
