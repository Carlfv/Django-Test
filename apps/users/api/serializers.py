from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'last_name')
#CODIGO OBSOLETO
# class UserTokenSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    #El siguiente serializador transforma todos los campos del modelo que se le indique en json
    class Meta:
        model = User #Modelo a serializar
        fields = '__all__' #campos a serializar

    #CREAR USUARIO VALIDADO
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])#SETEA EL PASSWORD
        user.save()
        return user
    


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'last_name')


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User

    #LISTADO DE USUARIOS
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'email': instance['email'],
            'name' : instance['name']
        }


