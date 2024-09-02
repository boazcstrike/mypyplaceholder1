"""domain layer"""

from decimal import Decimal
from uuid import UUID
from dataclasses import dataclass


@dataclass
class Account:
    """account class"""
    account_id: UUID
    customer_id: str
    account_number: str
    balance: Decimal

    def deposit(self, amount: Decimal):
        """deposit"""
        self.balance += amount

    def withdraw(self, amount: Decimal):
        """withdraw"""
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("U no money")

    def get_balance(self) -> Decimal:
        """get_balance"""
        return self.balance


@dataclass
class Customer:
    """customer class"""
    customer_id: str
    name: str
    email: str
    phone_number: str
