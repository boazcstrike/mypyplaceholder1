""" infrastructure layer """
from uuid import UUID
from typing import Optional

from models.main import Account, Customer


class AccountRepository:
    """ API for account entities """
    def __init__(self):
        self.accounts = {}
        self.customers = {}

    def save_customer(self, customer: Customer):
        """save_customer"""
        self.customers[customer.email] = customer

    def save_account(self, account: Account):
        """save_account"""
        self.accounts[account.account_id] = account

    def find_account_by_id(self, account_id: UUID) -> Account:
        """find_account_by_id"""
        return self.accounts[account_id]

    def find_accounts_by_customer_id(self, customer_id: UUID) -> list[Account]:
        """find_accounts_by_customer_id"""
        return [
            account for account in self.accounts.values()
            if account.customer_id == customer_id
        ]

    def find_customer_by_unique_key(
        self,
        email: str
    ) -> Optional[Customer]:
        """find_customer_by_unique_key

        Returns the Customer if found, or None if not.
        """
        return self.customers.get(email)
