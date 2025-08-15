from faker import Faker

fake = Faker()



def user_factory(role="USER"):
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

    return {
        "username": username,
        # "password": fake.password(
        #     length=12,
        #     special_chars=True,
        #     digits=True,
        #     upper_case=True,
        #     lower_case=True),
        "password": "Qa1@secure!", # 🔐 валидный пароль
        "role": role
    }



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