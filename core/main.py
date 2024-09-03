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
        if email in self.account_repository.customers:
            return self.account_repository.customers[email]

        customer_id = uuid4()
        customer = Customer(
            customer_id=customer_id,
            name=name,
            email=email,
            phone_number=phone_number,
        )
        self.account_repository.save_customer(customer)
        return customer

    def create_account(
        self,
        name: str,
        email: str,
        phone_number: str,
    ) -> Account:
        """create_account"""
        customer = self.create_customer(name, email, phone_number)
        account_id = uuid4()
        account_number = f"BO{str(account_id)[:12]}"
        account = Account(
            account_id=account_id,
            customer_id=customer.customer_id,
            account_number=account_number,
            balance=0,
        )
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

    def generate_account_statement(self, account_id: UUID) -> str:
        """generate_account_statement"""
        account = self.account_repository.find_account_by_id(account_id)
        statement = f"Account Number: {account.account_number}\n"
        statement += f"Customer ID: {account.customer_id}\n"
        statement += f"Balance: {account.get_balance()}\n"
        return statement
