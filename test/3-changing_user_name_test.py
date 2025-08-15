from utils.utils import assert_status
from data.factories import generation_name



class TestChangingUserName:
    def test_changing_user_name(
            self,
            update_customer_profile,
    ):
        """
        Test: Change the name of the user

        Steps:
            1. Generation new name.
            2. Fixture: update_customer_profile:
                - Create a new user.
                - Get auth header.
                - Change the name of the user.

        Expected result:
            Changing new name is successful.
        """
        new_name = generation_name()
        # print(new_name)  # Debag

        update_profile = update_customer_profile(new_name=new_name)
        # print(type(update_profile)) # Debag
        # print(update_profile.json()) # Debag
        assert_status(resp=update_profile, expected=200)

        data = update_profile.json()
        assert data.get('message') == 'Profile updated successfully'
        assert data.get('customer')['name'] == new_name, 'Имя профиля клиент не корретное/не изменилось'
        # print(update_profile.json()['customer']['name') # Debag

        print(f'\n ✅ Имя профиля клиента успешно изменено на: {data.get('customer')['name']}')

