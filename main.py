
import matplotlib as plt
import matplotlib.pyplot as plt
from Functions import *
from Classes import *

db_path = "sqlite:///finances.db"
db_creator = CreateDB(db_path)
data_functions = DataFunctions(db_creator.session)
user_input = UserInputs()
db_creator.create_tables()


def main():
    while True:
        print("\nOptions:")
        print("1. Add Record")
        print("2. Delete Record")
        print("3. Edit record")
        print("4. View Balance")
        print("5. View Records")
        print("6. View Sorted records")
        print("7. View Statistics")
        print("8. Finance Advices")
        print("9. Close")
            
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            record = data_functions.get_user_input()
            data_functions.add_record(record)
                
        elif choice == '2':
            data_functions.delete_record()
                
        elif choice == '3':
            record_id = int(input("Enter the ID of the record to edit: "))
            data_functions.edit_record(record_id)
            
        elif choice == '4':
            balance = data_functions.get_balance()
            print(f"\nYour balance is: ${balance:,.2f}".replace(",", " "))
                            
        elif choice == '5':
            while True:
                print("\nOptions:")
                print("1. View ALL Records")
                print("2. View Income Records")
                print("3. View Expense Records")
                print("4. View Record from date to date")
                print("5. Back to mainMenu") 
                                   
                view_choice = input("Enter your choice: ")
                
                if view_choice == "5":
                    break
                               
                elif view_choice == '1':
                    records = data_functions.get_all_records()
                    data_functions.display_records(records)
                    
                elif view_choice == '2':
                    records = data_functions.get_income_records()
                    data_functions.display_records(records)
        
                elif view_choice == '3':
                    records = data_functions.get_expense_records()
                    data_functions.display_records(records)
                    
                elif view_choice == '4':
                    start_date = user_input.take_date()
                    end_date = user_input.take_date()
                    data_functions.get_records_by_date(start_date, end_date)
                    
                else:
                    print("Invalid choice. Please try again.")
                                                
        elif choice == '6':
            records = data_functions.get_sorted_records()
            data_functions.display_records(records)
            

        elif choice == '7':
            while True:
                print("\nOptions:")
                print("1. View Weekly statistic")
                print("2. View Monthly statistic")
                print("3. View Year statistic")
                print("4. Back to mainMenu")
                
                statistic_choice = input("Enter your choice: ")
                
                if statistic_choice == '4':
                    break
   
                elif statistic_choice == '1':
                    data_functions.create_weekly_income_expense_chart()
        
                elif statistic_choice == '2':
                    data_functions.create_monthly_income_expense_chart()
                    
                elif statistic_choice == '3':
                    data_functions.create_yearly_income_expense_chart()
                    
                else:
                    print("Invalid choice. Please try again.") 
               
        elif choice == '8':
            data_functions.finance_advices()
                
        elif choice == '9':
            data_functions.close_session()
            break
        else:
            print("Invalid choice. Please try again.")
                
data_functions = DataFunctions(db_creator.session)
main()