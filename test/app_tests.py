import unittest

from mock import patch

from app import get_input_from_main_menu, main_application
from src.enumeration.main_menu import MainMenu
from src.exception.app_exceptions import MainMenuInputOutOfRange


class AppTests(unittest.TestCase):
    @patch('src.app.raw_input', lambda *args, **kwargs: '_')
    def test_none_numeric_input_from_main_menu_raises_value_error(self):
        self.assertRaises(ValueError, get_input_from_main_menu)

    @patch('src.app.raw_input', lambda *args, **kwargs: '999999')
    def test_input_value_out_of_range_from_main_menu_raises_main_menu_out_of_range_error(self):
        self.assertRaises(MainMenuInputOutOfRange, get_input_from_main_menu)

    @patch('src.app.raw_input', lambda *args, **kwargs: MainMenu.EXIT.value)
    def test_exit_option_exits_the_app(self):
        main_application()
