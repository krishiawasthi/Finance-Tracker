from main import ProfessionalFinanceTracker

def clear_screen():
    """Clear console screen"""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(title):
    """Print a professional header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def main():
    """Professional interactive CLI"""
    tracker = ProfessionalFinanceTracker()
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("  💰 PROFESSIONAL FINANCE TRACKER 💰")
        print("="*60)
        print("\n📌 MAIN MENU")
        print("1.  Add Income")
        print("2.  Add Expense")
        print("3.  View Summary")
        print("4.  View Expense Breakdown")
        print("5.  Monthly Report")
        print("6.  View All Transactions")
        print("7.  View Statistics")
        print("8.  Generate Chart")
        print("9.  Set Budget Limit")
        print("10. Export Data")
        print("11. Exit")
        
        choice = input("\nEnter your choice (1-11): ").strip()
        
        if choice == '1':
            print_header("ADD INCOME")
            category = input("Enter income category (e.g., Salary, Freelance): ").strip()
            try:
                amount = float(input("Enter amount: $"))
                description = input("Enter description (optional): ").strip()
                tracker.add_transaction(category, "Income", amount, description)
                input("\nPress Enter to continue...")
            except ValueError:
                print("❌ Invalid amount")
                input("\nPress Enter to continue...")
        
        elif choice == '2':
            print_header("ADD EXPENSE")
            print("Common categories: Groceries, Transport, Utilities, Entertainment, Healthcare, Other")
            category = input("\nEnter expense category: ").strip()
            try:
                amount = float(input("Enter amount: $"))
                description = input("Enter description (optional): ").strip()
                tracker.add_transaction(category, "Expense", amount, description)
                input("\nPress Enter to continue...")
            except ValueError:
                print("❌ Invalid amount")
                input("\nPress Enter to continue...")
        
        elif choice == '3':
            tracker.get_professional_summary()
            input("Press Enter to continue...")
        
        elif choice == '4':
            tracker.get_category_breakdown()
            input("Press Enter to continue...")
        
        elif choice == '5':
            tracker.get_monthly_report()
            input("Press Enter to continue...")
        
        elif choice == '6':
            tracker.show_all_transactions()
            input("Press Enter to continue...")
        
        elif choice == '7':
            tracker.get_statistics()
            input("Press Enter to continue...")
        
        elif choice == '8':
            tracker.plot_professional_chart()
            input("\nPress Enter to continue...")
        
        elif choice == '9':
            print_header("SET BUDGET LIMIT")
            category = input("Enter category name: ").strip()
            try:
                limit = float(input("Enter monthly budget limit: $"))
                tracker.set_budget(category, limit)
                input("\nPress Enter to continue...")
            except ValueError:
                print("❌ Invalid amount")
                input("\nPress Enter to continue...")
        
        elif choice == '10':
            print_header("EXPORT DATA")
            filename = input("Enter filename (or press Enter for auto): ").strip()
            if filename:
                tracker.export_to_csv(filename)
            else:
                tracker.export_to_csv()
            input("\nPress Enter to continue...")
        
        elif choice == '11':
            print("\n👋 Thank you for using Finance Tracker!")
            print("Your data has been saved. Goodbye!\n")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
