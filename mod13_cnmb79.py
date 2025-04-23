import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from main import validate_int_input, validate_date_input, get_symbol

class TestInputValidation(unittest.TestCase):

    def test_validate_chart_type(self):
        self.assertEqual(validate_int_input('1', (1, 2)), 1)
        self.assertEqual(validate_int_input('2', (1, 2)), 2)
        self.assertIsNone(validate_int_input('3', (1, 2)))
        self.assertIsNone(validate_int_input('a', (1, 2)))

    def test_validate_time_series(self):
        self.assertEqual(validate_int_input('1', (1, 4)), 1)
        self.assertEqual(validate_int_input('4', (1, 4)), 4)
        self.assertIsNone(validate_int_input('5', (1, 4)))
        self.assertIsNone(validate_int_input('xyz', (1, 4)))

    def test_validate_date_input(self):
        self.assertEqual(validate_date_input('2024-04-20'), datetime(2024, 4, 20))
        self.assertIsNone(validate_date_input('2024-13-01'))  
        self.assertIsNone(validate_date_input('04-20-2024')) 
        self.assertIsNone(validate_date_input('invalid'))

    @patch('builtins.input', side_effect=['IBM'])
    @patch('requests.get')
    def test_get_symbol_valid(self, mock_get, mock_input):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Global Quote": {
                "01. symbol": "IBM"
            }
        }
        mock_get.return_value = mock_response
        self.assertEqual(get_symbol(), 'IBM')

    @patch('builtins.input', side_effect=['FAKE', 'IBM'])
    @patch('requests.get')
    def test_get_symbol_invalid_then_valid(self, mock_get, mock_input):
        mock_response_invalid = MagicMock()
        mock_response_invalid.json.return_value = {}
        mock_response_valid = MagicMock()
        mock_response_valid.json.return_value = {
            "Global Quote": {
                "01. symbol": "IBM"}}
        mock_get.side_effect=[mock_response_invalid, mock_response_valid]
        self.assertEqual(get_symbol(), 'IBM')

if __name__ == '__main__':
    unittest.main()
