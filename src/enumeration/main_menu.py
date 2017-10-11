from enum import Enum


class MainMenu(Enum):
    __order__ = 'OPEN_CHASE_CSV_FILE OPEN_CITI_CSV_FILE EXIT'
    OPEN_CHASE_CSV_FILE = 1
    OPEN_CITI_CSV_FILE = 2
    EXIT = 3
