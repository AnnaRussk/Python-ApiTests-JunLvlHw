from utils.utils import assert_status
from data.factories import generation_name



class TestChangingUserName:
    def test_changing_user_name(
            self,
            create_account,
            get_customer_profile,
            update_customer_profile
    ):
        """
        Test: Change the name of the user

        Steps:
            1. Generation new name.
            2. Fixture: update_customer_profile:
                - Create a new user.
                - Get auth header.
                - Change the name of the user.
            3. Compare what new name different from the old

        Expected result:
            Changing new name is successful.
        """
        print(f' Test: Changing user name')       #Debag
        acc = create_account()
        auth = acc["auth_header"]

        # Имя ДО
        profile_before = get_customer_profile(auth)
        old_name = profile_before.get("name")

        # Меняем имя
        new_name = generation_name()
        update_profile = update_customer_profile(
            auth_header=auth,
            new_name=new_name
        )
        assert_status(resp=update_profile, expected=200)

        data = update_profile.json()
        assert data.get('message') == 'Profile updated successfully'
        assert data.get('customer')['name'] == new_name, 'Имя профиля клиент не корретное/не изменилось'

        # имя ПОСЛЕ
        profile_after = get_customer_profile(auth)
        assert profile_after["name"] == new_name
        assert old_name != new_name, "Новое имя совпало со старым"
        assert profile_after.get("name") == new_name, "Имя не обновилось"

        # Debag
        print(f'    ✅ Имя профиля клиента изменено. Старое "{old_name}" --> Новое "{new_name}"')


