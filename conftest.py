""" Fixtures for tests
"""

import requests, pytest
from data.urls import *
from utils.utils import assert_status
from data.factories import user_factory
from data.user import admin_headers




@pytest.fixture
def create_new_user():
    """
    Fixture: Verify login with valid credentials.

    Steps:
        1.  Create a new user.
        2.  Send a login request.
        3.  Validate the status and token.

    Expected result:
        New user successful created.

    Returns:
         dict{str, str} with "username" and "password" keys.
    """
    user_data = user_factory()
    new_user_resp = requests.post(
        url=STAGE + ADMIN_URI,
        headers=admin_headers,
        json=user_data
    )

    assert new_user_resp.url, "🌐 URL is empty!"
    assert_status(resp=new_user_resp, expected=201)

    user_name = new_user_resp.json().get("username")
    assert user_name, "👤 Username is empty!"
    # Stored login and password
    return {
        "username": user_data["username"],
        "password": user_data["password"]
    }



@pytest.fixture
def user_auth(create_new_user) -> dict:
    """ Fixture: Authorization user

        Expected result:
            Authorization is successful.

        Returns:
            login, headline of authorization
    """
    login_user_resp = requests.post(
        url=STAGE + LOGIN_URI,
        json=create_new_user
    )

    assert_status(resp=login_user_resp, expected=200)
    auth_header = login_user_resp.headers.get('Authorization')
    assert auth_header, "🔑 Authorization header is empty!"
    # Stored login and headline of authorization
    return {
        "auth_header": auth_header,
        "username": create_new_user,
    }


# Helper for account creation (fixture: create_account)
def create_account_data(user_auth):
    """
    Вспомогательная функция: создаёт аккаунт по переданным данным авторизации пользователя.

    Args:
        user_auth (dict): содержит 'auth_header' и 'username'

    Returns:
        dict: данные созданного аккаунта (account_id, auth_header, username)
    """
    create_account_resp = requests.post(
        url=STAGE + ACCOUNTS_URI,
        headers={
            'Authorization': user_auth["auth_header"]
        }
    )

    assert_status(resp=create_account_resp, expected=201)
    assert create_account_resp.json().get('balance') == 0.0, "💰 Initial balance is not zero!"
    assert not create_account_resp.json().get('transactions'), "📜 Transactions list is not empty!"
    account_id = create_account_resp.json().get('id')
    # Stored account id, login and headline of authorization
    return {
        "account_id": account_id,
        "auth_header": user_auth["auth_header"],
        "username": user_auth["username"]
    }



@pytest.fixture
# Create a new account and return account_id, auth_header, username
def create_account(user_auth):
    """
    Fixture: создаёт аккаунт для нового авторизованного пользователя.

    Returns:
        dict: данные аккаунта (account_id, auth_header, username)
    """
    return create_account_data(user_auth)



@pytest.fixture
def deposit_money(create_account):
    """
    Фабрика: Депозит на указанный счёт или на счёт из фикстуры 'create_account'.

    Параметры:
      - account_id: int | None
      - auth_header: str | None
      - amount: float (> 0)
    Возвращает: dict с id, auth_header, response
    """
    def _deposit(
            *,
            amount: float,
            account_id: int | None = None,
            auth_header: str | None = None
    ):
        assert amount > 0, "💥 Сумма депозита должна быть > 0"

        """ Если account_id и auth_header не передали явно — берём из create_account """
        acc_id = account_id if account_id is not None else create_account["account_id"]
        auth = auth_header if auth_header is not None else create_account["auth_header"]

        response = requests.post(
            url=STAGE + DEPOSIT_URI,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": auth,
            },
            json={
                "id": acc_id,
                "balance": amount
            }
        )

        assert_status(resp=response, expected=200)
        return {
            "id": acc_id,
            "auth_header": auth,
            "response": response
        }
    return _deposit



@pytest.fixture
def transfer_money():
    """
    Фикстура: позволяет выполнить перевод денег между двумя аккаунтами.

    Возвращает:
        Функцию _transfer

    _transfer принимает:
        sender_account_id (int): ID аккаунта отправителя.
        receiver_account_id (int): ID аккаунта получателя.
        amount (float): Сумма перевода (должна быть положительной).
        auth_header (str): Заголовок авторизации пользователя-отправителя.

    Возвращает:
        requests.Response: ответ API после выполнения перевода.
    """
    def _transfer(
            *,
            sender_account_id: int,
            receiver_account_id: int,
            amount: float,
            auth_header: str
    ):
        response = requests.post(
            url=STAGE + TRANSFER_URI,
            headers={"Authorization": auth_header, "Content-Type": "application/json"},
            json={
                "senderAccountId": sender_account_id,
                "receiverAccountId": receiver_account_id,
                "amount": amount
            }
        )
        return response
    return _transfer


@pytest.fixture
def update_customer_profile(user_auth):
    """
    Fixture:
    - возвращает функцию для обновления имени профиля.
    - Позволяет вызывать update_customer_profile(new_name="Имя") в тестах.
    """
    def _update(new_name:str="New name 1"):
        update_resp = requests.put(
            url=STAGE + CUSTOMER_URI,
            headers={"Authorization": user_auth["auth_header"]},
            json={"name": new_name}
        )
        # print(f'update_resp =', update_resp.json())  # Debug

        assert_status(resp=update_resp, expected=200)

        return update_resp

    return _update



