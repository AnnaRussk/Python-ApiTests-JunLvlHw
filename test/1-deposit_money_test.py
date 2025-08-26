from utils.utils import assert_status
from data.factories import generate_amount



class TestUpDeposit:
    def test_deposit_into_new_account(
            self,
            create_account,
            get_balance,
            deposit_money,
    ):
        """
        Step 1. Create new user. Фиктура: create_new_user
        Step 2. Authenticate user and return Basic Auth header. Фиктура: user_auth
        Step 3. Create a new account. Фиктура: create_account
        Step 4. Chek deposit before
        Step 5. Deposits money into the user's account. Фиктура: deposit_money
        Step 6. Chek deposit after
        Step 7. Compare what deposit before is equal deposit after
        """
        print(f' Test: Deposit money into new account')       #Debag
        acc = create_account()  # фабрика возвращает dict
        acc_id = acc["account_id"]
        auth = acc["auth_header"]

        # Баланс до депозита
        balance_before = get_balance(acc_id, auth)
        print(f"    💰 Баланс ДО: {balance_before}")       #Debag

        # Amount
        amount = generate_amount()
        assert amount > 0

        # Депозит
        deposit_resp = deposit_money(account_id=acc_id, auth_header=auth, amount=amount)
        assert_status(resp=deposit_resp["response"], expected=200)
        print(f"    ✅ Аккаунт юзера (id = {deposit_resp['id']}) пополнен на: {amount}")       #Debag
        # print(deposit_resp)       # Debag

        # Баланс после депозита
        balance_after = get_balance(acc_id, auth)
        print(f"    💰 Баланс ПОСЛЕ: {balance_after}")       #Debag
        assert deposit_resp["response"].json()["balance"] == amount

        # Проверка корректности баланса после пополнения
        assert balance_after == balance_before + amount, (
            f"❌ Баланс не совпадает: ожидали {balance_before + amount}, "
            f"а получили {balance_after}"
        )

        transactions = deposit_resp["response"].json().get('transactions', [])
        assert transactions, "📭 Список транзакций пуст"
        assert transactions[0]['amount'] == amount
