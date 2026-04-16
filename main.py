import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tabulate import tabulate
import os
import json

class ProfessionalFinanceTracker:
    """A professional personal finance tracker with advanced features"""
    
    def __init__(self, filename='finances.csv', budget_file='budget.json'):
        self.filename = filename
        self.budget_file = budget_file
        self.df = self.load_data()
        self.budgets = self.load_budgets()
    
    def load_data(self):
        """Load existing data or create new DataFrame"""
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        else:
            return pd.DataFrame(columns=['Date', 'Category', 'Type', 'Amount', 'Description'])
    
    def load_budgets(self):
        """Load budget limits for categories"""
        if os.path.exists(self.budget_file):
            with open(self.budget_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_budgets(self):
        """Save budget limits"""
        with open(self.budget_file, 'w') as f:
            json.dump(self.budgets, f, indent=2)
    
    def save_data(self):
        """Save data to CSV file"""
        self.df.to_csv(self.filename, index=False)
        print("✓ Data saved successfully")
    
    def add_transaction(self, category, transaction_type, amount, description=""):
        """Add a new transaction with validation"""
        try:
            amount = float(amount)
            if amount <= 0:
                print("❌ Amount must be greater than 0")
                return
            
            if not category or not category.strip():
                print("❌ Category cannot be empty")
                return
            
            new_row = pd.DataFrame({
                'Date': [datetime.now().strftime('%Y-%m-%d')],
                'Category': [category.strip()],
                'Type': [transaction_type],
                'Amount': [amount],
                'Description': [description.strip()]
            })
            
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            print(f"✓ Added {transaction_type}: ${amount:.2f} - {category}")
            self.save_data()
            
            # Check budget
            self.check_budget_alert(category, transaction_type, amount)
            
        except ValueError:
            print("❌ Invalid amount. Please enter a valid number.")
    
    def set_budget(self, category, limit):
        """Set a monthly budget limit for a category"""
        try:
            limit = float(limit)
            if limit <= 0:
                print("❌ Budget limit must be greater than 0")
                return
            
            self.budgets[category] = limit
            self.save_budgets()
            print(f"✓ Budget set for {category}: ${limit:.2f}")
        except ValueError:
            print("❌ Invalid budget amount")
    
    def check_budget_alert(self, category, transaction_type, amount):
        """Check if transaction exceeds category budget"""
        if transaction_type == 'Expense' and category in self.budgets:
            category_spending = self.get_category_spending(category)
            budget_limit = self.budgets[category]
            percentage = (category_spending / budget_limit) * 100
            
            if percentage >= 100:
                print(f"⚠️  WARNING: {category} budget EXCEEDED! ({percentage:.1f}%)")
            elif percentage >= 80:
                print(f"⚠️  ALERT: {category} budget at {percentage:.1f}%")
    
    def get_category_spending(self, category):
        """Get current month spending for a category"""
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        
        if len(self.df) == 0:
            return 0
        
        df_month = self.df[
            (self.df['Date'] >= month_start) & 
            (self.df['Category'] == category) &
            (self.df['Type'] == 'Expense')
        ]
        return df_month['Amount'].sum()
    
    def get_professional_summary(self):
        """Get detailed professional summary"""
        if len(self.df) == 0:
            print("\n📊 No transactions yet!\n")
            return
        
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        
        # This month
        df_month = self.df[self.df['Date'] >= month_start]
        income_month = df_month[df_month['Type'] == 'Income']['Amount'].sum()
        expenses_month = df_month[df_month['Type'] == 'Expense']['Amount'].sum()
        balance_month = income_month - expenses_month
        
        # All time
        income_total = self.df[self.df['Type'] == 'Income']['Amount'].sum()
        expenses_total = self.df[self.df['Type'] == 'Expense']['Amount'].sum()
        balance_total = income_total - expenses_total
        
        print("\n" + "="*60)
        print("💰 FINANCIAL SUMMARY")
        print("="*60)
        
        print(f"\n📅 THIS MONTH ({now.strftime('%B %Y')})")
        print("-" * 60)
        print(f"Income:       ${income_month:>12,.2f}")
        print(f"Expenses:     ${expenses_month:>12,.2f}")
        print(f"Balance:      ${balance_month:>12,.2f}")
        
        print(f"\n📈 ALL TIME")
        print("-" * 60)
        print(f"Total Income:    ${income_total:>10,.2f}")
        print(f"Total Expenses:  ${expenses_total:>10,.2f}")
        print(f"Total Balance:   ${balance_total:>10,.2f}")
        print("="*60 + "\n")
    
    def get_category_breakdown(self):
        """Show professional expense breakdown"""
        if len(self.df) == 0:
            print("\n📊 No data available\n")
            return
        
        expenses = self.df[self.df['Type'] == 'Expense']
        if len(expenses) == 0:
            print("\n📊 No expenses recorded\n")
            return
        
        category_totals = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        total_expenses = category_totals.sum()
        
        print("\n" + "="*60)
        print("📊 EXPENSE BREAKDOWN BY CATEGORY")
        print("="*60)
        
        table_data = []
        for category, amount in category_totals.items():
            percentage = (amount / total_expenses) * 100
            budget_info = ""
            
            if category in self.budgets:
                budget_limit = self.budgets[category]
                budget_status = "✓" if amount <= budget_limit else "✗ Over"
                budget_info = f"/ ${budget_limit:.2f} {budget_status}"
            
            table_data.append([category, f"${amount:.2f}", f"{percentage:.1f}%", budget_info])
        
        headers = ["Category", "Amount", "% of Total", "Budget Status"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal Expenses: ${total_expenses:.2f}\n")
    
    def get_monthly_report(self):
        """Generate monthly report"""
        if len(self.df) == 0:
            print("\n📋 No data available\n")
            return
        
        now = datetime.now()
        months_to_show = 6
        
        print("\n" + "="*70)
        print("📋 MONTHLY REPORT (Last 6 Months)")
        print("="*70)
        
        report_data = []
        
        for i in range(months_to_show):
            month_date = now - timedelta(days=30*i)
            month_start = datetime(month_date.year, month_date.month, 1)
            
            if i < months_to_show - 1:
                month_end = datetime(month_date.year, month_date.month + 1, 1) if month_date.month < 12 else datetime(month_date.year + 1, 1, 1)
            else:
                month_end = now
            
            df_period = self.df[(self.df['Date'] >= month_start) & (self.df['Date'] < month_end)]
            
            income = df_period[df_period['Type'] == 'Income']['Amount'].sum()
            expenses = df_period[df_period['Type'] == 'Expense']['Amount'].sum()
            balance = income - expenses
            
            report_data.append([
                month_start.strftime('%B %Y'),
                f"${income:.2f}",
                f"${expenses:.2f}",
                f"${balance:.2f}"
            ])
        
        headers = ["Month", "Income", "Expenses", "Balance"]
        print(tabulate(report_data, headers=headers, tablefmt="grid"))
        print()
    
    def show_all_transactions(self):
        """Display all transactions in a professional table"""
        if len(self.df) == 0:
            print("\n📋 No transactions yet!\n")
            return
        
        print("\n" + "="*80)
        print("📋 ALL TRANSACTIONS")
        print("="*80 + "\n")
        
        display_df = self.df.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:.2f}")
        
        print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=False))
        print()
    
    def export_to_csv(self, filename=None):
        """Export data to a new CSV file"""
        if filename is None:
            filename = f"finances_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        self.df.to_csv(filename, index=False)
        print(f"✓ Data exported to {filename}")
    
    def plot_professional_chart(self):
        """Create professional visualization"""
        if len(self.df) == 0:
            print("❌ No data to plot!")
            return
        
        expenses = self.df[self.df['Type'] == 'Expense']
        if len(expenses) == 0:
            print("❌ No expenses to plot!")
            return
        
        category_totals = expenses.groupby('Category')['Amount'].sum()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Bar chart
        axes[0].bar(category_totals.index, category_totals.values, color='steelblue')
        axes[0].set_title('Expenses by Category', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Category', fontsize=12)
        axes[0].set_ylabel('Amount ($)', fontsize=12)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Pie chart
        axes[1].pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
        axes[1].set_title('Expense Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('professional_expense_chart.png', dpi=300)
        print("✓ Professional chart saved as 'professional_expense_chart.png'")
        plt.show()
    
    def get_statistics(self):
        """Get detailed statistics"""
        if len(self.df) == 0:
            print("\n📊 No data available\n")
            return
        
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        df_month = self.df[self.df['Date'] >= month_start]
        
        # Calculate metrics
        avg_expense = df_month[df_month['Type'] == 'Expense']['Amount'].mean()
        highest_expense = df_month[df_month['Type'] == 'Expense']['Amount'].max()
        total_transactions = len(df_month)
        
        print("\n" + "="*60)
        print("📊 STATISTICS")
        print("="*60)
        print(f"Total Transactions (This Month): {total_transactions}")
        print(f"Average Expense: ${avg_expense:.2f}")
        print(f"Highest Single Expense: ${highest_expense:.2f}")
        print(f"Total Categories: {df_month['Category'].nunique()}")
        print("="*60 + "\n")


if __name__ == "__main__":
    tracker = ProfessionalFinanceTracker()
    
    print("Personal Finance Tracker - Demo\n")
    
    # Add sample transactions
    tracker.add_transaction("Salary", "Income", 4500, "Monthly salary")
    tracker.add_transaction("Groceries", "Expense", 250, "Weekly groceries")
    tracker.add_transaction("Transport", "Expense", 100, "Gas and parking")
    tracker.add_transaction("Entertainment", "Expense", 75, "Movie and dinner")
    tracker.add_transaction("Utilities", "Expense", 150, "Electricity and water")
    tracker.add_transaction("Freelance", "Income", 800, "Side project")
    
    # Set budgets
    tracker.set_budget("Groceries", 300)
    tracker.set_budget("Entertainment", 100)
    
    # Display reports
    tracker.get_professional_summary()
    tracker.get_category_breakdown()
    tracker.get_monthly_report()
    tracker.show_all_transactions()
    tracker.get_statistics()
    tracker.plot_professional_chart()
