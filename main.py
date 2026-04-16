import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class FinanceTracker:
    """A simple personal finance tracker"""
    
    def __init__(self, filename='finances.csv'):
        self.filename = filename
        self.df = self.load_data()
    
    def load_data(self):
        """Load existing data or create new DataFrame"""
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        else:
            return pd.DataFrame(columns=['Date', 'Category', 'Type', 'Amount', 'Description'])
    
    def save_data(self):
        """Save data to CSV file"""
        self.df.to_csv(self.filename, index=False)
        print(f"✓ Data saved to {self.filename}")
    
    def add_transaction(self, category, transaction_type, amount, description=""):
        """Add a new transaction"""
        new_row = {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Category': category,
            'Type': transaction_type,
            'Amount': amount,
            'Description': description
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        print(f"✓ Added {transaction_type}: ${amount} ({category})")
        self.save_data()
    
    def get_summary(self):
        """Get income and expense summary"""
        if len(self.df) == 0:
            print("No transactions yet!")
            return
        
        income = self.df[self.df['Type'] == 'Income']['Amount'].sum()
        expenses = self.df[self.df['Type'] == 'Expense']['Amount'].sum()
        balance = income - expenses
        
        print("\n" + "="*40)
        print("FINANCE SUMMARY")
        print("="*40)
        print(f"Total Income:   ${income:.2f}")
        print(f"Total Expenses: ${expenses:.2f}")
        print(f"Balance:        ${balance:.2f}")
        print("="*40 + "\n")
    
    def get_category_breakdown(self):
        """Show expenses by category"""
        if len(self.df) == 0:
            print("No transactions yet!")
            return
        
        expenses = self.df[self.df['Type'] == 'Expense']
        if len(expenses) == 0:
            print("No expenses yet!")
            return
        
        category_totals = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        print("\nExpense Breakdown by Category:")
        print("-" * 40)
        for category, amount in category_totals.items():
            print(f"{category:20s} ${amount:8.2f}")
        print("-" * 40 + "\n")
    
    def plot_expenses(self):
        """Create a visualization of expenses by category"""
        if len(self.df) == 0:
            print("No data to plot!")
            return
        
        expenses = self.df[self.df['Type'] == 'Expense']
        if len(expenses) == 0:
            print("No expenses to plot!")
            return
        
        category_totals = expenses.groupby('Category')['Amount'].sum()
        
        plt.figure(figsize=(10, 6))
        category_totals.plot(kind='bar', color='steelblue')
        plt.title('Expense Breakdown by Category', fontsize=14, fontweight='bold')
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Amount ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('expense_chart.png')
        print("✓ Chart saved as 'expense_chart.png'")
        plt.show()
    
    def show_all_transactions(self):
        """Display all transactions"""
        if len(self.df) == 0:
            print("No transactions yet!")
            return
        
        print("\nAll Transactions:")
        print(self.df.to_string(index=False))
        print()


if __name__ == "__main__":
    tracker = FinanceTracker()
    
    print("Personal Finance Tracker\n")
    
    tracker.add_transaction("Salary", "Income", 3000, "Monthly salary")
    tracker.add_transaction("Groceries", "Expense", 150, "Weekly groceries")
    tracker.add_transaction("Transport", "Expense", 50, "Gas and parking")
    tracker.add_transaction("Entertainment", "Expense", 30, "Movie tickets")
    tracker.add_transaction("Utilities", "Expense", 100, "Electricity bill")
    
    tracker.get_summary()
    tracker.get_category_breakdown()
    tracker.show_all_transactions()
    tracker.plot_expenses()
