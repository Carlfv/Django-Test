from audioop import reverse
from rest_framework.test import APITestCase
from faker import Faker
from rest_framework import status


class TestSetUp(APITestCase):

    def setUp(self):
        from apps.users.models import User
        faker = Faker()
        self.register_url = '/clientes/'
        self.login_url = '/login/'
        self.user = User.objects.create_superuser(
            email= faker.email(),
            name= 'UserTest',
            last_name= 'Testeando',
            password= 'tester12345'
        )
        response = self.client.post(
            self.login_url,
            {
                'email':self.user.email,
                'password': 'tester12345'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token= response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)
        return super().setUp()

    def test_login(self):
        print(self.token)