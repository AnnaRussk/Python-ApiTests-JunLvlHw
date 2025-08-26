""" Fixtures for tests
"""

import requests, pytest, time
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

    resp = requests.post(
        url=STAGE + ADMIN_URI,
        headers=admin_headers,
        json=user_data.model_dump()
    )

    assert resp.url, "🌐 URL is empty!"
    assert_status(resp=resp, expected=201)

    user_name = resp.json().get("username")
    assert user_name, "👤 Username is empty!"

    # Stored login and password
    return user_data



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
        json=create_new_user.model_dump()
    )

    assert_status(resp=login_user_resp, expected=200)

    auth_header = login_user_resp.headers.get('Authorization')
    assert auth_header, "🔑 Authorization header is empty!"

    # Stored login and headline of authorization
    return {
        "auth_header": auth_header,
        "username": create_new_user.username,
    }



@pytest.fixture
def create_account(user_auth):
    """
    Factory: создаёт аккаунт и возвращает dict.
    Вызов:
        acc = create_account()                   # с user_auth
        acc = create_account(auth_header="...")  # можно подменить токен
    """
    def _create(auth_header: str | None = None) -> dict:
        auth = auth_header or user_auth["auth_header"]      # Выбор заголовка — либо из user_auth, либо явный

        resp = requests.post(
            url=STAGE + ACCOUNTS_URI,
            headers={"Authorization": auth}
        )
        assert_status(resp=resp, expected=201)

        data = resp.json()
        assert data.get("balance") == 0.0, "💰 Initial balance is not zero!"
        assert not data.get("transactions"), "📜 Transactions list is not empty!"

        return {
            "account_id": data.get("id"),
            "auth_header": auth,
            "username": user_auth["username"],
        }

    return _create      # Возвращаем функцию (фабрику)



@pytest.fixture
def get_balance():
    """
    Fixture/Factory:  Get balance by account id
    Expected result: Current balance by account
    Returns: float
    """
    def _balance(account_id: int, auth_header: str, retries: int = 1, delay: float = 0.5) -> float:
        """Вернуть баланс счёта из /customer/accounts.
        retries/delay опциональны: позволяют подождать консистентности.
        """

        for i in range(max(1, retries)):
            request = requests.get(
                url=STAGE + CUSTOMER_ACCOUNTS_URI,
                headers={"Authorization": auth_header},
            )
            assert_status(request, 200)

            items = request.json()  # список аккаунтов

            for accounts in items:
                if accounts.get("id") == account_id:
                    balance = accounts.get("balance")
                    assert balance is not None, "В ответе нет поля balance"
                    return round(float(balance), 2)

            # Если не нашли и есть ещё попытки — подождём и попробуем снова
            if i + 1 < retries:
                time.sleep(delay)

        raise AssertionError(f"Счёт {account_id} не найден в /customer/accounts")

    return _balance



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

        amount = round(float(amount), 2)

        assert amount > 0, "💥 Сумма депозита должна быть > 0"

        # Если account_id не передан — создаём аккаунт через фабрику (можно передать кастомный auth_header)
        if account_id is None:
            account = create_account(auth_header)
            acc_id = account["account_id"]
            auth = account["auth_header"]
        else:
            assert auth_header is not None, "🔑 Нужен auth_header для указанного account_id"
            acc_id = account_id
            auth = auth_header

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

        amount = round(float(amount), 2)

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
def get_customer_profile():
    """
    Fixture factory: получить профиль юзера по auth_header.
    """
    def _profile(auth_header: str) -> dict:
        resp = requests.get(
            url=STAGE + CUSTOMER_URI,
            headers={"Authorization": auth_header}
        )
        assert_status(resp, 200)

        return resp.json()
    return _profile



@pytest.fixture
def update_customer_profile(user_auth):
    """
    Fixture:
    Factory: обновить имя профиля по конкретному auth_header.
    Вызов: resp = update_customer_profile_for(auth_header, new_name)
    """
    def _update(auth_header: str, new_name:str):
        response = requests.put(
            url=STAGE + CUSTOMER_URI,
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            },
            json={"name": new_name}
        )
        # print(f'response =', response.json())  # Debug
        assert_status(resp=response, expected=200)

        return response
    return _update



