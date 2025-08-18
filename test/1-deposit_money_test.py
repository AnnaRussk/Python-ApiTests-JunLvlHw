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
    def test_deposit_money_into_new_account(
            self,
            create_account,
            get_balance,
            deposit_money,
    ):
        """
        Step 1. Create new user. Фиктура: create_new_user
        Step 2. Authenticate user and return Basic Auth header. Фиктура: user_auth
        Step 3. Create a new account. Фиктура: create_account
        Step 4. Deposits money into the user's account. Фиктура: deposit_money
        """
        acc = create_account()  # фабрика возвращает dict
        acc_id = acc["account_id"]
        auth = acc["auth_header"]

        # Баланс до депозита
        balance_before = get_balance(acc_id, auth)
        print(f"\n    💰 Баланс ДО: {balance_before}")

        amount = generate_amount()
        # Депозит
        deposit_resp = deposit_money(account_id=acc_id, auth_header=auth, amount=amount)

        assert_status(resp=deposit_resp["response"], expected=200)
        # Баланс после депозита
        balance_after = get_balance(acc_id, auth)
        print(f"    💰 Баланс ПОСЛЕ: {balance_after}")
        assert deposit_resp["response"].json()["balance"] == amount
        # Проверка баланса
        assert balance_after == balance_before + amount, (
            f"❌ Баланс не совпадает: ожидали {balance_before + amount}, "
            f"а получили {balance_after}"
        )

        transactions = deposit_resp["response"].json().get('transactions', [])
        assert transactions, "📭Список транзакций пуст"
        assert transactions[0]['amount'] == amount

        print(f"✅ Депозит юзера (id = {deposit_resp['id']}) пополнен успешно на: {amount}")
        # print(deposit_resp)       # Debag
