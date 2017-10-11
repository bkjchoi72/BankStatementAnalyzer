import pandas
from abc import ABCMeta, abstractmethod


class Statement(object):
    __metaclass__ = ABCMeta

    def __init__(self, path_to_csv_file):
        self.loaded_csv = pandas.read_csv(path_to_csv_file)

    def get_first_5_rows_of_csv(self):
        return self.loaded_csv.head()

