from utils.utils import assert_status
from data.factories import generate_amount, generate_transfer_amount



class TestUpTransfer:
    def test_transfer_between_accounts(
        self,
        user_auth,
        transfer_money,
        deposit_money,
        create_account,
        get_balance,
    ):
        """
        Title
            Test "Transfer money from one user account to another".
        Steps
            1. Сreate account receiver
            2. Сreate the sender account and add balance
            3. Transfer of funds
            4. Check balance. Compare what BEFORE and AFTER has changed by the amount
                of transfer from sender to receiver
        """
        print(f' Test: Transfer money from account to another')
        deposit_amount = generate_amount()
        transfer_amount = generate_transfer_amount()

        # Step 1.
        receiver_account = create_account()
        # print("\nReceiver:", receiver_account["account_id"])      # Debag

        # Step 2.
        deposit_response = deposit_money(amount=deposit_amount)
        sender_data = deposit_response
        # print("Sender:", sender_data.items())     # Debag
        assert deposit_amount >= transfer_amount, f"Желаемая сумма пеервода больше текущего баланса "

        assert_status(resp=deposit_response, expected=200)
        assert deposit_response["response"].json()["balance"] == deposit_amount

        # Balance before transfer
        balance_before_from = get_balance(sender_data["id"], sender_data["auth_header"])
        assert balance_before_from > 0, \
            (f"    ❌ Начальный баланс: отправителя {balance_before_from} отрицательный. "
             f"Перед переводом необходиом пополнить баланс!")
        balance_before_to = get_balance(receiver_account["account_id"], receiver_account["auth_header"])
        # Debag
        print(f'    💰 Начальный баланс: ОТПРАВИТЕЛЬ = {balance_before_from} | ПОЛУЧАТЕЛЬ = {balance_before_to}')

        # Step 3.
        transfer_response = transfer_money(
            sender_account_id=sender_data["id"],
            receiver_account_id=receiver_account["account_id"],
            amount=transfer_amount,
            auth_header=sender_data["auth_header"]
        )

        # print("Transfer response:", transfer_response.json())     # Debag
        data = transfer_response.json()
        assert_status(resp=transfer_response, expected=200)
        assert data['message'] == 'Transfer successful', 'Transfer is NOT successful'
        assert data['amount'] == transfer_amount
        # Debag
        print(f"    ✅ Перевод в размере {data['amount']}"
              f" успешно выполнен между аккаунтами(id): {data['senderAccountId']}"
              f" --> {data['receiverAccountId']}")

        # Step 3.
        # Balance after transfer
        balance_after_from = get_balance(sender_data["id"], sender_data["auth_header"], retries=3, delay=0.5)
        balance_after_to = get_balance(receiver_account["account_id"], receiver_account["auth_header"], retries=3, delay=0.5)

        # Rounding up to 2 signs
        assert round(balance_after_from, 2) == round(balance_before_from - transfer_amount, 2)
        assert round(balance_after_to, 2) == round(balance_before_to + transfer_amount, 2)

        # Debag
        print(f'    💰 Текущий Баланс: ОТПРАВИТЕЛЬ '
              f'(id {transfer_response.json()['senderAccountId']}) = {balance_after_from} | '
              f'ПОЛУЧАТЕЛЬ (id {transfer_response.json()['receiverAccountId']}) = {balance_after_to}')
