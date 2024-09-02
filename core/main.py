""" use case """
from uuid import uuid4, UUID
from decimal import Decimal
from models.main import (
    Account, Customer,
)


class UseCase:
    """use case class"""
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_customer(
        self,
        name: str,
        email: str,
        phone_number: str,
    ) -> Customer:
        """create_customer"""
        existing_customer = self.account_repository.find_customer_by_unique_key(
            name, phone_number, email
        )
        if existing_customer:
            return existing_customer

        customer_id = uuid4()
        customer = Customer(customer_id, name, email, phone_number)
        self.account_repository.save_customer(customer)
        return customer

    def create_account(
        self,
        name: str,
        email: str,
        phone_number: str,
        *args,
    ):
        """create_account"""
        customer = self.create_customer(name, email, phone_number)
        self.account_repository.save_customer(customer)
        account_id = uuid4()
        account_number = f"BOAZ{str(account_id)[:12]}"
        account = Account(account_id, customer.customer_id, account_number, 0)
        self.account_repository.save_account(account)
        return account

    def make_transaction(
        self,
        account_id: UUID,
        amount: Decimal,
        transaction_type: str,
    ):
        """make_transaction"""
        account = self.account_repository.find_account_by_id(account_id)
        if transaction_type == "deposit":
            account.deposit(amount)
        elif transaction_type == "withdraw":
            account.withdraw(amount)
        self.account_repository.save_account(account)

    def generate_account_statement(self, account_id: UUID):
        """generate_account_statement"""
        account = self.account_repository.find_account_by_id(account_id)
        statement = f"Account Number: {account.account_number}\n"
        statement += f"Customer ID: {account.customer_id}\n"
        statement += f"Balance: {account.get_balance()}\n"
        return statement
