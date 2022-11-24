from urllib import response
from tests.test_setup import TestSetUp
from tests.data.users.user_data import UserData
from rest_framework import status

class UserTestCase(TestSetUp):
    
    
    def test_search_user(self):
        user = UserData().build_user_JSON()
        response = self.client.post(
            '/usuario/users/',
            user,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
