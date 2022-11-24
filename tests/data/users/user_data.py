from faker import Faker

from apps.users.models import User

faker = Faker()

class UserData:
    
    def build_user_JSON(self):
        return {'email' : faker.email(),
                'name' : faker.name(),
                'last_name' : faker.last_name(),
                'password' : 'testeando123'}

    def create_user(self):
        return User.objects.create_user()
