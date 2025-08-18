from utils.utils import assert_status



class TestUpTransfer:
    def test_transfer_money_from_account_to_another(
        self,
        user_auth,
        transfer_money,
        deposit_money,
        create_account,
        get_balance,
        transfer_amount: float = 33
    ):
        """
        Test: Transfer money from one user account to another
        """

        """ Шаг 1: создаём аккауатн-получателя """
        receiver_account = create_account()
        # print("\nReceiver:", receiver_account["account_id"])      # Debag

        """ Шаг 2-3:  создаём аккауатн-отправителя и пополняем счёт отправителя """
        deposit_response = deposit_money(amount=333)
        sender_data = deposit_response
        # print("Sender:", sender_data.items())     # Debag

        assert_status(resp=deposit_response, expected=200)
        assert deposit_response["response"].json()["balance"] == 333

        # Balance before transfer
        balance_before_from = get_balance(sender_data["id"], sender_data["auth_header"])
        balance_before_to = get_balance(receiver_account["account_id"], receiver_account["auth_header"])
        print(f'\n    💰 Начальный баланс: отправителя = {balance_before_from} | получателя = {balance_before_to}')

        """ Шаг 4: перевод средств от отправителя к получателю """
        transfer_response = transfer_money(
            sender_account_id=sender_data["id"],
            receiver_account_id=receiver_account["account_id"],
            amount=transfer_amount,
            auth_header=sender_data["auth_header"]
        )
        # print("Transfer response:", transfer_response.json())     # Debag
        assert_status(resp=transfer_response, expected=200)
        assert transfer_response.json()['message'] == 'Transfer successful', 'Transfer is NOT successful'
        assert transfer_response.json()['amount'] == transfer_amount

        # Balance after transfer
        balance_after_from = get_balance(sender_data["id"], sender_data["auth_header"], retries=3, delay=0.5)
        balance_after_to = get_balance(receiver_account["account_id"], receiver_account["auth_header"], retries=3, delay=0.5)

        # Check that balance before and after has changed by the amount of transfer from sender to receiver
        assert balance_after_from == balance_before_from - transfer_amount
        assert balance_after_to == balance_before_to + transfer_amount

        print(f'    💰 Текущий Баланс: отправителя (id {transfer_response.json()['senderAccountId']}) = {balance_after_from} | '
              f'получателя (id {transfer_response.json()['receiverAccountId']}) = {balance_after_to}')
        print(f"✅ Перевод в размере {transfer_response.json()['amount']}"
              f" успешно выполнен между аккаунтами: {transfer_response.json()['senderAccountId']}"
              f" -> {transfer_response.json()['receiverAccountId']}")
