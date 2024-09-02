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

    def test_api_find_by_account_id(self):
        """
        Test saving an account and retrieving it by ID.
        """
        for i in range(5):
            account = self.use_case.create_account(
                f"Customer {i}", f"customer{i}@example.com", f"12345678{i}")
            self.account_repository.save_account(account)
            retrieved_account = self.account_repository.find_account_by_id(
                account.account_id)
            self.assertEqual(retrieved_account, account)
            self.assertEqual(retrieved_account.account_id, account.account_id)
            self.assertEqual(retrieved_account.customer_id, account.customer_id)

    def test_api_find_customer_id(self):
        """
        Test saving an account and retrieving it by ID.
        """
        for i in range(5):
            # try to add 3 accounts for one customer
            for _ in range(3):
                account = self.use_case.create_account(
                    f"Customer {i}",
                    f"customer{i}@example.com",
                    f"12345678{i}",
                )
                self.account_repository.save_account(account)


if __name__ == '__main__':
    unittest.main()
