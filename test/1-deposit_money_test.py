from utils.utils import assert_status
import random

def generate_amount(max_digits=4):
    """
    Генерирует случайную сумму типа float с ограничением по общему количеству знаков (цифр).
    Пример: max_digits=4 → может быть 12.3, 1.23, 999.9 и т.д.
    """
    while True:
        amount = round(random.uniform(1, 9999), 2)  # 2 знака после запятой
        if len(str(amount).replace('.', '').replace(',', '')) <= max_digits:
            return amount


class TestUpDeposit:
    def test_deposit_money_into_new_account(self, deposit_money):
        """
        Step 1. Create new user. Фиктура: create_new_user
        Step 2. Authenticate user and return Basic Auth header. Фиктура: user_auth
        Step 3. Create a new account. Фиктура: create_account
        Step 4. Deposits money into the user's account. Фиктура: deposit_money
        """
        amount = generate_amount()
        deposit_resp = deposit_money(amount=amount)

        assert_status(resp=deposit_resp, expected=200)
        assert deposit_resp["response"].json()["balance"] == amount
        transactions = deposit_resp["response"].json().get('transactions', [])
        assert transactions, "📭Список транзакций пуст"
        assert transactions[0]['amount'] == amount

        print(f'\n ✅ Депозит юзера пополнен успешно на: {amount}')
        # print(deposit_resp)       # Debag
