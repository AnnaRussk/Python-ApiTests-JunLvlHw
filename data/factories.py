from faker import Faker
import random
from models.CreateUserRequest import CreateUserRequest


fake = Faker()



def user_factory(role="USER") -> CreateUserRequest:
    """
    Генерирует тестового пользователя с валидными username, password и role.
    """
    prefix = "aqa"
    max_len = 15

    """ Генерируем случайное имя и оставляем только буквы/цифры """
    rest = ''.join(ch for ch in fake.user_name() if ch.isalnum())

    """ Урезаем или дополняем до нужной длины """
    rest = rest[:max_len - len(prefix)]
    username = prefix + rest

    return CreateUserRequest(
        username=username,
        password="Qa1@secure!",     # 🔐 Всегда валидный пароль. Через генерацию НЕвсегда
        role=role
    )



def users_factory(role: str = "USER", count: int = 1) -> list[dict]:
    """
    Фабрика: генерирует список тестовых пользователей.

    Args:
        role: роль пользователя (по умолчанию "USER").
        count: сколько пользователей сгенерировать.

    Returns:
        Список словарей с ключами username, password, role.
    """
    prefix = "aqa"
    max_len = 15

    def _make_one() -> dict:
        rest = ''.join(ch for ch in fake.user_name() if ch.isalnum())
        rest = rest[:max_len - len(prefix)]
        username = prefix + rest
        return {
            "username": username,
            "password": "Qa1@secure!",
            "role": role
        }

    users = []
    for _ in range(count):
        users.append(_make_one())
    return users
    # return [_make_one() for _ in range(count)]




def generation_name():
    """
    Генерирует случайное имя.
    """
    prefix = "QA"
    max_len = 8

    # Генерируем логин и оставляем только буквы и цифры
    rest = ''.join(ch for ch in fake.user_name() if ch.isalnum())

    # Урезаем или дополняем до нужной длины
    rest = rest[:max_len - len(prefix)]
    profile_name = prefix + rest

    return profile_name



def generate_amount(max_digits: int = 4) -> float:
    if not isinstance(max_digits, int) or max_digits <= 0:
        raise ValueError("max_digits должен быть положительным целым")
    while True:
        amount = round(random.uniform(1, 9999), 2)
        # считаем ВСЕ цифры (целая+дробная), точку не считаем
        if len(str(amount).replace('.', '').replace(',', '')) <= max_digits:
            return amount



def generate_transfer_amount(max_digits: int = 2) -> float:
    # Переиспользуем логику generate_amount, но по умолчанию строже
    return generate_amount(max_digits=max_digits)