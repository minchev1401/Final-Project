from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Finance(Base):
    __tablename__ = 'finances'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date)
    amount = Column(Float)
    type = Column(String)


    
class CreateDB:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        self.session = None

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        if not self.session.query(Finance).first():
            self.fill_starting_data()

    def fill_starting_data(self):
        starting_records = [
            Finance(name='Starting balance', description='', date=datetime(2024, 1, 31), amount=10000, type='Income'),
            Finance(name='Salary', description='Monthly salary', date=datetime(2024, 2, 1), amount=4000, type='Income'),
            Finance(name='Rent', description='Rent for cottage', date=datetime(2024, 2, 2), amount=1200, type='Expense'),
            Finance(name='Electricity', description='', date=datetime(2024, 2, 3), amount=200, type='Expense'),
            Finance(name='Cinema', description='', date=datetime(2024, 2, 5), amount=100, type='Expense'),
            Finance(name='Car services', description='Change oil and filters', date=datetime(2024, 2, 10), amount=650, type='Expense'),
            Finance(name='Aquapark', description='fun by the pool', date=datetime(2024, 2, 11), amount=300, type='Expense'),
            Finance(name='Market', description='shopping', date=datetime(2024, 2, 12), amount=150, type='Expense'),
            Finance(name='Phone repair', description='broken screen', date=datetime(2024, 2, 13), amount=70, type='Expense'),
            Finance(name='Rent from apartmants', description='mountly rent', date=datetime(2024, 2, 13), amount=2000, type='Income'),
            Finance(name='Salary', description='February salary', date=datetime(2024, 3, 1), amount=4000, type='Income'),
            Finance(name='Rent', description='Rent for cottage', date=datetime(2024, 3, 1), amount=1200, type='Expense'),
            Finance(name='Electricity', description='February', date=datetime(2024, 3, 2), amount=250, type='Expense'),
            Finance(name='Market', description='shopping', date=datetime(2024, 3, 3), amount=65, type='Expense'),
            Finance(name='New Phone', description='', date=datetime(2024, 3, 15), amount=1500, type='Expense'),
            Finance(name='Salary', description='March salary', date=datetime(2024, 3, 15), amount=4000, type='Income'),
            Finance(name='Market', description='shopping', date=datetime(2024, 3, 16), amount=236.23, type='Expense'),
            Finance(name='Rent', description='Rent for cottage', date=datetime(2024, 3, 16), amount=1200, type='Expense'),
            Finance(name='Electricity', description='Vilage Bilss', date=datetime(2024, 3, 17), amount=250.56, type='Expense'),
            Finance(name='Bike', description='New bike for son', date=datetime(2024, 3, 17), amount=700, type='Expense'),
            Finance(name='Rent from apartmants', description='mountly rent', date=datetime(2024, 3, 17), amount=2500, type='Income'),
            Finance(name='Lotary', description='wining ticket', date=datetime(2024, 3, 18), amount=20000, type='Income'),
            Finance(name='Vacantion', description='holydays', date=datetime(2024, 3, 18), amount=2555.90, type='Expense'),
            Finance(name='Trip', description='Trip with the famely', date=datetime(2024, 3, 19), amount=1154.33, type='Expense'),
            Finance(name='Cinema', description='fun', date=datetime(2024, 3, 19), amount=248.50, type='Expence'),
            Finance(name='Salary', description='March salary', date=datetime(2024, 3, 20), amount=4000, type='Income'),
            Finance(name='Car services', description='roof_repair', date=datetime(2024, 3, 20), amount=650, type='Expense'),
            Finance(name='Market', description='shopping', date=datetime(2024, 3, 20), amount=150.34, type='Expense'),
            Finance(name='Market', description='', date=datetime(2024, 3, 22), amount=163.25, type='Expense'),
            Finance(name='Market', description='shopping', date=datetime(2024, 3, 20), amount=150, type='Expense'),
            Finance(name='Market', description='shopping', date=datetime(2024, 3, 20), amount=150, type='Expense'),
        ]
        self.session.add_all(starting_records)
        self.session.commit()
        print("Records added successfully.")
    
class UserInputs:
    def take_date(self):
        while True:
            date_entry = input("Enter the date in YYYY-MM-DD format: ")
            try:
                year, month, day = map(int, date_entry.split('-'))
                date = datetime(year, month, day)
                break
            except (ValueError, OverflowError):
                print("Invalid date format. Please try again using YYYY-MM-DD format.")
        return date
               
    def take_amount(self):
        while True:
            amount_entry = input("Enter the amount: ")
            try:
                amount = float(amount_entry)
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
        return amount
            
    def take_record_type(self):
        while True:
            record_type = input("Enter the type (Income/Expense): ").capitalize()
            if record_type in ['Income', 'Expense']:
                break
            else:
                print("Invalid type. Please enter 'Income' or 'Expense'.")
        return record_type

class IncomeRecord:
    def __init__(self, name, description, date, amount):
        self.name = name
        self.description = description
        self.date = date
        self.amount = amount
        self.type = 'Income'

class ExpenseRecord:
    def __init__(self, name, description, date, amount):
        self.name = name
        self.description = description
        self.date = date
        self.amount = amount
        self.type = 'Expense'
        
