"""unit tests"""

import unittest
from uuid import UUID
from decimal import Decimal
from models.main import (
    Account,
)
from api.main import AccountRepository
from core.main import UseCase


class TestBankingSystem(unittest.TestCase):
    """
    Test class for the banking system.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        self.account_repository = AccountRepository()
        self.use_case = UseCase(self.account_repository)

    def test_create_account(self):
        """
        Test the creation of a new account.
        """
        account = self.use_case.create_account(
            "John Doe", "john.doe@example.com", "1234567890"
        )
        self.assertIsInstance(account, Account)
        self.assertIsInstance(account.customer_id, UUID)
        self.assertIsInstance(account.account_id, UUID)
        self.assertEqual(account.balance, Decimal(0))

    def test_make_deposit(self):
        """
        Test making a deposit into an account.
        """
        account = self.use_case.create_account(
            "John Doe", "john.doe@example.com", "1234567890"
        )
        self.use_case.make_transaction(
            account.account_id, Decimal(1000.0), 'deposit')
        self.assertEqual(account.get_balance(), Decimal(1000.0))

    def test_make_withdrawal(self):
        """
        Test making a withdrawal from an account.
        """
        account = self.use_case.create_account(
            "John Doe", "john.doe@example.com", "1234567890"
        )
        self.use_case.make_transaction(
            account.account_id, Decimal(1000.75), 'deposit')
        self.use_case.make_transaction(
            account.account_id, Decimal(500.25), 'withdraw')
        self.assertEqual(account.get_balance(), Decimal(500.50))

    def test_withdrawal_with_insufficient_funds(self):
        """
        Test making a withdrawal with insufficient funds in the account.
        """
        account = self.use_case.create_account(
            "John Doe", "john.doe@example.com", "1234567890"
        )
        with self.assertRaises(ValueError):
            self.use_case.make_transaction(
                account.account_id, Decimal(1000), 'withdraw')

    def test_generate_account_statement(self):
        """
        Test generating an account statement.
        """
        account = self.use_case.create_account(
            "John Doe", "john.doe@example.com", "1234567890"
        )
        self.use_case.make_transaction(
            account.account_id, Decimal(1000.0), 'deposit')
        self.use_case.make_transaction(
            account.account_id, Decimal(500.0), 'withdraw')
        statement = self.use_case.generate_account_statement(
            account.account_id)
        self.assertIn(f"Account Number: {account.account_number}", statement)
        self.assertIn(f"Customer ID: {account.customer_id}", statement)
        self.assertIn(f"Balance: {account.get_balance()}", statement)

    def test_multiple_accounts_transactions(self):
        """
        Test creating multiple accounts and making withdrawals from them.
        """
        accounts = [
            self.use_case.create_account(
                f"Customer {i}", f"customer{i}@example.com", f"12345678{i}")
            for i in range(5)
        ]

        for account in accounts:
            self.use_case.make_transaction(
                account.account_id, Decimal(1000.0), 'deposit')
            self.use_case.make_transaction(
                account.account_id, Decimal(500.0), 'withdraw')
            self.assertEqual(account.get_balance(), Decimal(500.0))

        insufficient_funds_account = accounts[0]
        with self.assertRaises(ValueError):
            self.use_case.make_transaction(
                insufficient_funds_account.account_id,
                Decimal(1000.0),
                'withdraw')

    def test_api_find_account_by_id(self):
        """
        Test saving an account and retrieving it by ID.
        """
        for i in range(5):
            account = self.use_case.create_account(
                f"John Doe {i}", f"customer{i}@example.com", f"12345678{i}")
            self.account_repository.save_account(account)
            retrieved_account = self.account_repository.find_account_by_id(
                account.account_id)
            self.assertEqual(retrieved_account, account)
            self.assertEqual(retrieved_account.account_id, account.account_id)
            self.assertEqual(retrieved_account.customer_id, account.customer_id)

    def test_api_find_customer_by_unique_key(self):
        """
        Test saving a customer and retrieving it by email.
        """
        customer_name = "John Doe"
        customer_email = "johndoe@gmail.com"
        customer_phone = "1234567890"

        # create 5 accounts
        accounts = []
        for _ in range(5):
            account = self.use_case.create_account(
                customer_name,
                customer_email,
                customer_phone,
            )
            accounts.append(account)

        customer = self.account_repository.find_customer_by_unique_key(customer_email)
        self.assertEqual(customer.email, customer_email, "Customer email should match")

    def test_api_one_customer_find_accounts_by_customer_id(self):
        """
        Test saving one customer and multiple accounts and find accounts by customer id
        """
        customer_name = "John Doe"
        customer_email = "johndoe@gmail.com"
        customer_phone = "1234567890"

        # create 5 accounts
        accounts = []
        for _ in range(5):
            account = self.use_case.create_account(
                customer_name,
                customer_email,
                customer_phone,
            )
            accounts.append(account)

        customer = self.account_repository.find_customer_by_unique_key(customer_email)
        customer_accounts = self.account_repository.find_accounts_by_customer_id(
            customer.customer_id
        )

        # number of find accounts by customer
        self.assertEqual(
            5,
            len(customer_accounts),
            "Number of accounts in repository should match")

        # accounts should be in accounts repository
        for account in accounts:
            self.assertIn(
                account,
                self.account_repository.accounts.values(),
                "Account should be in the list of created accounts")

        # only one customer
        self.assertEqual(
            1,
            len(self.account_repository.customers),
            "Only one customer should be in the repository")

    def test_api_multiple_customers_find_accounts_by_customer_id(self):
        """
        Test saving multiple accounts and find accounts by customer id
        """
        customers = []

        # create 10 customers
        for i in range(10):
            customer_name = "John Doe"+str(i)
            customer_email = "johndoe@gmail.com"+str(i)
            customer_phone = "1234567890"

            # create 5 accounts per customer
            customer_accounts = []
            for _ in range(5):
                account = self.use_case.create_account(
                    customer_name,
                    customer_email,
                    customer_phone,
                )

            customer = self.account_repository.find_customer_by_unique_key(customer_email)
            customers.append(customer)
            customer_accounts = self.account_repository.find_accounts_by_customer_id(
                customer.customer_id
            )

            # number of 5 customer accounts should match find accounts by customer
            self.assertEqual(
                5,
                len(customer_accounts),
                "Number of accounts in repository should match")

            # accounts should be in accounts repository
            for account in customer_accounts:
                self.assertIn(
                    account,
                    self.account_repository.accounts.values(),
                    "Account should be in the list of created accounts")

        # all customers in repository
        for customer in customers:
            self.assertIn(
                customer,
                self.account_repository.customers.values(),
                "Customer should be in the list of created customers")

        # number of 50 total customers accounts should match
        self.assertEqual(
            50,
            len(self.account_repository.accounts),
            "Number of accounts in repository should match")

        # number of 10 total customers should match
        self.assertEqual(
            10,
            len(self.account_repository.customers),
            "Only one customer should be in the repository")


if __name__ == '__main__':
    unittest.main()
