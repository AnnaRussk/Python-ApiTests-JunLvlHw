"""Проверка статус-кода"""
def assert_status(resp, expected):
    if isinstance(resp, dict):
        resp = resp.get("response")
        if resp is None:
            raise TypeError("⚠️ assert_status received dict without 'response' key")
    assert resp.status_code == expected, (
        f"❌ Ожидался статус {expected}, но пришёл {resp.status_code}. "
        f"Тело ответа: {resp.text}"
    )