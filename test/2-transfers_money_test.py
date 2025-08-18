from utils.utils import assert_status



class TestUpTransfer:
    def test_transfer_money_from_account_to_another(
        self,
        user_auth,
        transfer_money,
        deposit_money,
        create_account,
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

        print(f"\n ✅ Перевод в размере {transfer_response.json()['amount']}"
              f" успешно выполнен между аккаунтами: {transfer_response.json()['senderAccountId']}"
              f" -> {transfer_response.json()['receiverAccountId']}")
