import tkinter as tk
from tkinter import messagebox
import datetime
import math
import random
import csv

def load_accounts_from_csv(filepath):
    accounts = {}
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                account_number = row.get('account_number')
                account_holder = row.get('account_holder')
                balance = float(row.get('balance', 0.0))
                if account_number and account_holder:
                    accounts[account_number] = BankAccount(account_number, account_holder, balance)
    except FileNotFoundError:
        pass
    return accounts


class BankAccount:
    def __init__(self, account_number, account_holder, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self):
        return self.balance
    
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")
        self.accounts = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Account Number:").grid(row=0, column=0)
        self.account_number_entry = tk.Entry(self.root)
        self.account_number_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Account Holder:").grid(row=1, column=0)
        self.account_holder_entry = tk.Entry(self.root)
        self.account_holder_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Create Account", command=self.create_account).grid(row=2, columnspan=2)

        tk.Label(self.root, text="Amount:").grid(row=3, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Deposit", command=self.deposit).grid(row=4, column=0)
        tk.Button(self.root, text="Withdraw", command=self.withdraw).grid(row=4, column=1)

        tk.Button(self.root, text="Check Balance", command=self.check_balance).grid(row=5, columnspan=2)

    def create_account(self):
        account_number = self.account_number_entry.get()
        account_holder = self.account_holder_entry.get()
        
        if not account_number or not account_holder:
            messagebox.showerror("Error", "Account number and holder name cannot be empty.")
            return
        
        if account_number in self.accounts:
            messagebox.showerror("Error", "Account already exists.")
            return
        
        new_account = BankAccount(account_number, account_holder)
        self.accounts[account_number] = new_account
        messagebox.showinfo("Success", f"Account created for {account_holder}.")

    def deposit(self):
        account_number = self.account_number_entry.get()
        amount = float(self.amount_entry.get())
        
        if account_number not in self.accounts:
            messagebox.showerror("Error", "Account does not exist.")
            return
        
        try:
            self.accounts[account_number].deposit(amount)
            messagebox.showinfo("Success", f"Deposited {amount} to {account_number}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        account_number = self.account_number_entry.get()
        amount = float(self.amount_entry.get())
        
        if account_number not in self.accounts:
            messagebox.showerror("Error", "Account does not exist.")
            return
        
        try:
            self.accounts[account_number].withdraw(amount)
            messagebox.showinfo("Success", f"Withdrew {amount} from {account_number}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    def check_balance(self):
        account_number = self.account_number_entry.get()
        
        if account_number not in self.accounts:
            messagebox.showerror("Error", "Account does not exist.")
            return
        
        balance = self.accounts[account_number].get_balance()
        messagebox.showinfo("Balance", f"Balance for {account_number}: {balance}")
def main():
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()
