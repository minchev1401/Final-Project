import unittest
from unittest.mock import Mock, patch
from Functions import DataFunctions
from Classes import Finance, UserInputs, IncomeRecord, ExpenseRecord, CreateDB
from datetime import datetime
import io
from datetime import datetime
import numpy as np


class TestCreateDB(unittest.TestCase):
    def setUp(self):
        self.db_path = 'sqlite:///test_db.sqlite'
        self.db = CreateDB(self.db_path)

    def test_create_tables(self):

        self.db.create_tables()
        self.assertIsNotNone(self.db.session)


    def test_fill_starting_data(self):

        self.db.create_tables()
        self.db.fill_starting_data()

        finance_records = self.db.session.query(Finance).all()
        self.assertGreater(len(finance_records), 0)

class TestDataFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        self.data_functions = DataFunctions(session=self.mock_session)
        self.finance = Finance()
    
    @patch('builtins.print')
    def test_get_balance_success(self, mock_print):
    
        mock_income_records = [
            Finance(amount=100, type='Income'),
            Finance(amount=200, type='Income'),
            ]
        
        mock_expense_records = [
            Finance(amount=50, type='Expense'),
            Finance(amount=75, type='Expense'),
            ]

        self.mock_session.query.return_value.filter_by.return_value.all.side_effect = [mock_income_records, mock_expense_records]

        result = self.data_functions.get_balance()

        self.mock_session.query.assert_called_with(Finance)

        expected_balance = np.sum([record.amount for record in mock_income_records]) - np.sum([record.amount for record in mock_expense_records])
        self.assertEqual(result, expected_balance)

        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_get_balance_exception(self, mock_print):
        self.data_functions.session.query.side_effect = Exception("Test exception")

        result = self.data_functions.get_balance()

        expected_message = "An unexpected error occurred: Test exception"
        mock_print.assert_called_once_with(expected_message)

        self.assertIsNone(result)    

    @patch('builtins.print')
    def test_get_all_records_success(self, mock_print):
        
        mock_records = [
            Finance(id=1, amount=100, type='Income'),
            Finance(id=2, amount=50, type='Expense'),
        ]

        self.mock_session.query.return_value.all.return_value = mock_records

        result = self.data_functions.get_all_records()

        self.mock_session.query.assert_called_once_with(Finance)

        self.assertEqual(result, mock_records)
        
    @patch('builtins.print')
    def test_get_all_records_exception(self, mock_print):

        self.mock_session.query.side_effect = Exception("Test exception")

        result = self.data_functions.get_all_records()

        expected_message = "An unexpected error occurred: Test exception"
        mock_print.assert_called_once_with(expected_message)

        self.assertIsNone(result)
     
    @patch('builtins.print')    
    def test_get_income_records_success(self, mock_print):
        
        mock_income_records = [
            Finance(amount=50, type='Income'),
            Finance(amount=75, type='Income'),
        ]

        self.mock_session.query.return_value.filter_by.return_value.all.return_value = mock_income_records

        result = self.data_functions.get_income_records()

        self.mock_session.query.assert_called_with(Finance)

        expected_message = f"\nTotal Income is: $125.00"
        mock_print.assert_called_once_with(expected_message)

        self.assertEqual(result, mock_income_records)
        
    @patch('builtins.print')
    def test_get_income_records_exception(self,mock_print):

        self.mock_session.query.side_effect = Exception("Test exception")

        result = self.data_functions.get_income_records()

        expected_message = "An unexpected error occurred: Test exception"
        mock_print.assert_called_once_with(expected_message)

        self.assertIsNone(result)
     
    @patch('builtins.print')    
    def test_get_expense_records_success(self, mock_print):
        
        mock_expense_records = [
            Finance(amount=50, type='Expense'),
            Finance(amount=75, type='Expense'),
        ]

        self.mock_session.query.return_value.filter_by.return_value.all.return_value = mock_expense_records

        result = self.data_functions.get_expense_records()

        self.mock_session.query.assert_called_with(Finance)

        expected_message = f"\nTotal Expense is: $125.00"
        mock_print.assert_called_once_with(expected_message)

        self.assertEqual(result, mock_expense_records)
        
    @patch('builtins.print')
    def test_get_expense_records_exception(self,mock_print):

        self.mock_session.query.side_effect = Exception("Test exception")

        result = self.data_functions.get_expense_records()

        expected_message = "An unexpected error occurred: Test exception"
        mock_print.assert_called_once_with(expected_message)

        self.assertIsNone(result)
   
    @patch('builtins.print')
    def test_add_record_success(self, mock_print):

        mock_record = IncomeRecord(name='Salary', description='Monthly salary', date='2024-03-01', amount=1000)
        self.data_functions.add_record(mock_record)

        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        
    @patch('builtins.print')   
    def test_add_record_exception(self, mock_print):

        self.mock_session.add.side_effect = Exception("Test exception")

        self.data_functions.add_record(Finance())

        expected_message = "An unexpected error occurred: Test exception"
        mock_print.assert_called_once_with(expected_message)

        self.mock_session.rollback.assert_called_once()
               
    def test_display_records(self):
        records = [
            Finance(id=1, name='Record 1', description='Description 1', date=datetime(2024, 3, 1), amount=100, type='Income'),
            Finance(id=2, name='Record 2', description='Description 2', date=datetime(2024, 3, 2), amount=200, type='Expense')
        ]
        expected_output = """\
   ID       Name     Description        Date  Amount     Type
0   1  Record 1  Description 1  01-03-2024     100  Income
1   2  Record 2  Description 2  02-03-2024     200  Expense
"""

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.data_functions.display_records(records)
            actual_output = mock_stdout.getvalue()

            expected_lines = expected_output.strip().split()
            actual_lines = actual_output.strip().split()
            self.assertEqual(len(expected_lines), len(actual_lines))

            for expected_line, actual_line in zip(expected_lines, actual_lines):
                self.assertEqual(expected_line.strip(), actual_line.strip())

    def test_close_session(self):

        self.data_functions.close_session()

        self.assertTrue(self.data_functions.session.closed)
        
    def test_get_records_by_date(self):

        mock_records = [Finance(id=1, name='Record 1', description='Description 1', date=datetime(2024, 1, 1), amount=100, type='Income'),
                        Finance(id=2, name='Record 2', description='Description 2', date=datetime(2024, 1, 31), amount=200, type='Expense')]
        self.data_functions.session.query.return_value.filter.return_value = mock_records

        start_date = '2024-01-01'
        end_date = '2024-01-31'
        result = self.data_functions.get_records_by_date(start_date, end_date)

        self.assertEqual(result, mock_records)

    def test_get_records_by_date_exception(self):

        self.data_functions.session.query.side_effect = Exception('Database error')

        start_date = '2024-01-01'
        end_date = '2024-01-31'
        result = self.data_functions.get_records_by_date(start_date, end_date)

        self.assertIsNone(result)
      
    @patch('builtins.input', side_effect=['Alice', 'Dinner out', '2024-03-18', "50", 'Expense'])
    def test_get_user_input_expense(self,record):
        record = ['Alice', 'Dinner out', '2024-03-18', '50', 'Expense']
        result = DataFunctions.get_user_input(record)
        self.assertIsInstance(result, ExpenseRecord)
        self.assertEqual(result.name, 'Alice')
        self.assertEqual(result.description, 'Dinner out')
        self.assertEqual(result.amount, 50)
        self.assertEqual(result.date.strftime('%Y-%m-%d'), '2024-03-18')
        
    @patch('Classes.Finance')
    @patch('builtins.print')
    def test_create_weekly_income_expense_chart(self, mock_print, mock_finance):

        mock_income1 = mock_finance(date=datetime(2024, 3, 15), amount=100, type='Income')
        mock_income2 = mock_finance(date=datetime(2024, 3, 17), amount=200, type='Income')
        mock_expense1 = mock_finance(date=datetime(2024, 3, 16), amount=50, type='Expense')
        mock_expense2 = mock_finance(date=datetime(2024, 3, 18), amount=75, type='Expense')

        self.data_functions.session.query.return_value.filter.return_value.all.return_value = [
            mock_income1, mock_income2, mock_expense1, mock_expense2
        ]

    @patch('builtins.input', side_effect=['1'])
    def test_delete_record(self, mock_input):
 
        mock_record = Finance(id=1)

        self.data_functions.session.query.return_value.filter.return_value.first.return_value = mock_record

        self.data_functions.session.commit = unittest.mock.Mock()

        self.data_functions.delete_record()

        self.data_functions.session.delete.assert_called_once_with(mock_record)

class TestUserInputs(unittest.TestCase):
    @patch('builtins.input', side_effect=['2024-03-01'])
    def test_take_date_valid(self, mock_input):
        user_inputs = UserInputs()
        expected_date = datetime(2024, 3, 1)
        self.assertEqual(user_inputs.take_date(), expected_date)

    @patch('builtins.input', side_effect=['invalid_date', '2024-03-01'])
    def test_take_date_invalid_then_valid(self, mock_input):
        user_inputs = UserInputs()
        expected_date = datetime(2024, 3, 1)
        self.assertEqual(user_inputs.take_date(), expected_date)

    @patch('builtins.input', side_effect=['1000'])
    def test_take_amount_valid(self, mock_input):
        user_inputs = UserInputs()
        expected_amount = 1000.0
        self.assertEqual(user_inputs.take_amount(), expected_amount)

    @patch('builtins.input', side_effect=['invalid_amount', '1000'])
    def test_take_amount_invalid_then_valid(self, mock_input):
        user_inputs = UserInputs()
        expected_amount = 1000.0
        self.assertEqual(user_inputs.take_amount(), expected_amount)

    @patch('builtins.input', side_effect=['Income'])
    def test_take_record_type_valid(self, mock_input):
        user_inputs = UserInputs()
        expected_type = 'Income'
        self.assertEqual(user_inputs.take_record_type(), expected_type)

    @patch('builtins.input', side_effect=['invalid_type', 'Income'])
    def test_take_record_type_invalid_then_valid(self, mock_input):
        user_inputs = UserInputs()
        expected_type = 'Income'
        self.assertEqual(user_inputs.take_record_type(), expected_type)
        

if __name__ == '__main__':
    unittest.main()
