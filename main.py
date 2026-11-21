import data_manager
import analysis
import reports

def main():
    data = data_manager.load_data()

    while True:
        print("\\n===================================")
        print("       STUDENT BUDGET MANAGER")
        print("===================================")
        print("1. Add Transaction")
        print("2. Display Transactions")
        print("3. Search Transaction")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Summary Report")
        print("7. Data Analysis (NumPy + Pandas)")
        print("8. Python Data Structures")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            data = data_manager.add_record(data)
        elif choice == "2":
            data_manager.display_records(data)
        elif choice == "3":
            data_manager.search_record(data)
        elif choice == "4":
            data = data_manager.update_record(data)
        elif choice == "5":
            data = data_manager.delete_record(data)
        elif choice == "6":
            reports.summary_report(data)
        elif choice == "7":
            analysis.analyze_data(data)
        elif choice == "8":
            data_manager.show_data_structures(data)
        elif choice == "9":
            print("Thank you for using Student Budget Manager!")
            break
        else:
            print("Invalid choice. Please enter 1 to 9.")

if __name__ == "__main__":
    main()
