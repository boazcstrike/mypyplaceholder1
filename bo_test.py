"""answers"""
import random

from api.main import AccountAPI
from core.main import UseCase


def initialize_use_case():
    """Initializes the use case with an account repository."""
    account_repository = AccountAPI()
    return UseCase(account_repository)


def create_account(use_case_instance):
    """Creates an account and returns it."""
    return use_case_instance.create_account(
        "John Doe", "johndoe@gmail.com", "1234567890"
    )


def randomize_amount(min_amount, max_amount):
    """Returns a random amount between min_amount and max_amount."""
    return random.randint(min_amount, max_amount)


def perform_test_transactions(use_case_instance, account):
    """Performs deposit and withdrawal transactions."""
    print("\nDepositing 3 times")
    for _ in range(3):
        amount = randomize_amount(1000, 10000)
        print(f"Init deposit {amount}")
        use_case_instance.make_transaction(
            account.account_id, amount, "deposit")
        generate_account_statement(use_case_instance, account.account_id)

    print("\nWithdrawing 3 times")
    for _ in range(3):
        amount = randomize_amount(0, 1000)
        print(f"Init withdraw {amount}")
        use_case_instance.make_transaction(
            account.account_id, amount, "withdraw")
        generate_account_statement(use_case_instance, account.account_id)

    print("\nAttempting to withdraw invalid amount")
    print("Init withdraw 30001")
    try:
        use_case_instance.make_transaction(
            account.account_id, 30001, "withdraw")
    except ValueError as e:
        print(f"Error: {e}")
    generate_account_statement(use_case_instance, account.account_id)


def generate_account_statement(use_case_instance, account_id):
    """Generates and prints the account statement."""
    statement = use_case_instance.generate_account_statement(account_id)
    print(statement, "\n")


def main():
    """Main function to run the tests."""
    use_case_instance = initialize_use_case()
    account = create_account(use_case_instance)
    print(f"New account created: {account.account_number}\n")

    perform_test_transactions(use_case_instance, account)


main()
