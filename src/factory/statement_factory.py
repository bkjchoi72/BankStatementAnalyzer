from src.enumeration.bank import Bank
from src.chase_statement import ChaseStatement
from src.citi_statement import CitiStatement


class StatementFactory(object):
    @staticmethod
    def make_statement(bank, path_to_csv_file):
        if bank == Bank.CHASE:
            return ChaseStatement(path_to_csv_file)
        elif bank == Bank.CITI:
            return CitiStatement(path_to_csv_file)
