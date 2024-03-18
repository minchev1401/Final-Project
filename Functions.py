import numpy as np
import pandas as pd
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Classes import *

class DataFunctions:
    def __init__(self, session):
        self.session = session

    def add_record(self, record):
        try:
            record = Finance(
                name=record.name,
                description=record.description,
                date=record.date,
                amount=record.amount,
                type=record.type
            )
            self.session.add(record)
            self.session.commit()
            print("Record added successfully!")
        except Exception as e:
            self.session.rollback()
            print(f"An unexpected error occurred: {e}")

    def get_user_input(self):
        
        try:            
            user_inputs = UserInputs()
            name = input("Enter the name: ")
            description = input("Enter the description: ")
            date = user_inputs.take_date()
            amount = user_inputs.take_amount()
            record_type = user_inputs.take_record_type()

            return IncomeRecord(name, description, date, amount) if record_type == 'Income' else ExpenseRecord(name, description, date, amount)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def edit_record(self, record_id):
        try:
            record_id_input = input("Enter the ID of the record to edit (or 'exit' to cancel): ")
            if record_id_input.lower() == 'exit':
                print("Operation cancelled.")
                return

            record_id = int(record_id_input)
            finance_record = self.session.query(Finance).filter(Finance.id == record_id).first()

            if finance_record:
                print(f"Editing record with ID {record_id}:")
                name = input(f"Enter new name ({finance_record.name}): ")
                description = input(f"Enter new description ({finance_record.description}): ")

                while True:
                    date_entry = input(f"Enter new date in DD-MM-YYYY format ({finance_record.date}): ")
                    try:
                        year, month, day = map(int, date_entry.split('-'))
                        date = datetime(year, month, day)
                        break
                    except ValueError:
                        print("Invalid date format. Please try again using DD-MM-YYYY format.")

                while True:
                    amount_entry = input(f"Enter new amount ({finance_record.amount}): ")
                    try:
                        amount = float(amount_entry)
                        break
                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")

                while True:
                    record_type = input(f"Enter new type (Income/Expense) ({finance_record.type}): ").capitalize()
                    if record_type in ["Income", "Expense"]:
                        break
                    else:
                        print("Invalid type. Please enter 'Income' or 'Expense'.")

                finance_record.name = name
                finance_record.description = description
                finance_record.date = date
                finance_record.amount = amount
                finance_record.type = record_type


                self.session.commit()
                print(f"Record with ID {record_id} updated successfully.")
            else:
                print(f"Record with ID {record_id} not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
                      
    def get_balance(self):
        try:
            income_records = self.session.query(Finance).filter_by(type='Income').all()
            expense_records = self.session.query(Finance).filter_by(type='Expense').all()

            total_income = np.sum([record.amount for record in income_records])
            total_expense = np.sum([record.amount for record in expense_records])

            balance = total_income - total_expense 
            return balance
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
                
    def finance_advices(self):
        try:
            balance = self.get_balance()
            if_no_income = balance / 30

            if balance > 0:
                print("\n1. Save at least '20%' of your income for savings.")
                print("2. Allocate funds for any outstanding debts.")
                print("3. Consider investing the surplus.")
            elif balance < 0:
                print("\n1. Review your expenses and cut unnecessary spending.")
                print("2. Prioritize paying off high-interest debts.")
                print("3. Create a budget to manage your expenses.")
            else:
                print("\n1. Maintain your balanced budget.")
                print("2. Continue tracking your income and expenses.")
                
            print(f"\nIf you don't have any 'Income' next 30 days, you will have ${if_no_income:.2f} per day!\n")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def create_weekly_income_expense_chart(self):

        today = datetime.today().date()
        start_date = today - timedelta(days=7)
        end_date = today

        incomes = self.session.query(Finance).filter(Finance.date.between(start_date, end_date), Finance.type == 'Income').all()
        expenses = self.session.query(Finance).filter(Finance.date.between(start_date, end_date), Finance.type == 'Expense').all()
        
        income_dates, income_amounts = zip(*[(income.date, income.amount) for income in incomes])
        expense_dates, expense_amounts = zip(*[(expense.date, expense.amount) for expense in expenses])

        plt.figure(figsize=(10, 6))
        plt.plot(income_dates, income_amounts, label='Income', marker='o')
        plt.plot(expense_dates, expense_amounts, label='Expense', marker='x')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Weekly Income vs. Expense')
        plt.legend()
        plt.grid(True)
        plt.show()

    def create_monthly_income_expense_chart(self):

        today = datetime.today().date()
        start_date = today - timedelta(days=30)
        end_date = today

        incomes = self.session.query(Finance).filter(Finance.date.between(start_date, end_date), Finance.type == 'Income').all()
        expenses = self.session.query(Finance).filter(Finance.date.between(start_date, end_date), Finance.type == 'Expense').all()

        income_dates, income_amounts = zip(*[(income.date, income.amount) for income in incomes])
        expense_dates, expense_amounts = zip(*[(expense.date, expense.amount) for expense in expenses])

        plt.figure(figsize=(10, 6))
        plt.plot(income_dates, income_amounts, label='Income', marker='o')
        plt.plot(expense_dates, expense_amounts, label='Expense', marker='x')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Monthly Income vs. Expense')
        plt.legend()
        plt.grid(True)
        plt.show()

    def create_yearly_income_expense_chart(self):

        today = datetime.today().date()
        start_date = today - timedelta(days=365)
        end_date = today

        incomes = self.session.query(Finance).filter(Finance.date.between(start_date, end_date), Finance.type == 'Income').all()
        expenses = self.session.query(Finance).filter(Finance.date.between(start_date, end_date), Finance.type == 'Expense').all()

        income_dates, income_amounts = zip(*[(income.date, income.amount) for income in incomes])
        expense_dates, expense_amounts = zip(*[(expense.date, expense.amount) for expense in expenses])

        plt.figure(figsize=(10, 6))
        plt.plot(income_dates, income_amounts, label='Income', marker='o')
        plt.plot(expense_dates, expense_amounts, label='Expense', marker='x')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Yearly Income vs. Expense')
        plt.legend()
        plt.grid(True)
        plt.show()

    def delete_record(self):
        while True:
            try:
                record_id_input = input("Enter the ID of the record to delete (or 'exit' to cancel): ")
                if record_id_input.lower() == 'exit':
                    print("Delete operation cancelled.")
                    break

                record_id = int(record_id_input)
                record = self.session.query(Finance).filter(Finance.id == record_id).first()

                if record:

                    deleted_id = record.id

                    self.session.delete(record)
                    self.session.commit()

                    print("Record deleted successfully:")

                    self.session.query(Finance).filter(Finance.id > deleted_id).update({Finance.id: Finance.id - 1})
                    self.session.commit()

                    break
                else:
                    print("Record not found. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid integer ID.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
    def get_all_records(self):
        try:
            all_records = self.session.query(Finance).all()
            return all_records
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    def get_income_records(self):
        try:
            income_records = self.session.query(Finance).filter_by(type='Income').all()
            total_income = sum(record.amount for record in income_records)
            print(f"\nTotal Income is: ${total_income:,.2f}".replace(",", " "))
            return income_records
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_expense_records(self):
        try:
            expense_records = self.session.query(Finance).filter_by(type='Expense').all()
            total_expenses = sum(record.amount for record in expense_records)
            print(f"\nTotal Expense is: ${total_expenses:,.2f}".replace(",", " "))
            return expense_records
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def get_sorted_records(self):
        while True:
            sort_by_input = input("Enter the sorting option ('date' or 'amount) or 'exit' to cancel: ").lower()
            if sort_by_input in ['date', 'amount']:
                break
            elif sort_by_input == 'exit':
                break
            else:
                print("\nInvalid sorting option")

        sort_by = sort_by_input
        if sort_by == 'date':
            records = self.session.query(Finance).order_by(Finance.date).all()
            
        else:
            records = self.session.query(Finance).order_by(Finance.amount).all()
        return records
          
    def display_records(self, records):
        if not records:
            print("No records found.")
            return

        data = [{
            'ID': record.id,
            'Name': record.name,
            'Description': record.description,
            'Date': record.date.strftime('%d-%m-%Y'),
            'Amount': record.amount,
            'Type': record.type
        } for record in records]
        df = pd.DataFrame(data)
        print(df)
        
    def close_session(self):
        self.session.close()
        print("Session closed.")
        
    def get_records_by_date(self, start_date, end_date):
        try:
            filtered_records = self.session.query(Finance).filter(Finance.date.between(start_date, end_date))
            self.display_records(filtered_records)
            return filtered_records
        
        except Exception as e:
            print(f"Error filtering records: {e}")
            return None