from ast import Return
from datetime import datetime
import email
from urllib import request
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session #Libreria que maneja las sesiones de usuario
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.api.serializers import CustomTokenObtainPairSerializer, CustomUserSerializers

from apps.users.models import User


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate( #devuelve un usuario desde la base de datos con los parametros
            username = username,
            password = password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializers(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de session correcto'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o Usuario incorrecto'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o Usuario incorrecto'}, status=status.HTTP_400_BAD_REQUEST)

class Logout(GenericAPIView): #Clase que recibe el usuario y vuelve a generar un token
    #Esta funcion valida la id del usuario para actualizar el token que se haya estado utilizando
    def post(self, request, *args, **kgwars):
        user = User.objects.filter(id = request.data.get('user', 0)) #
        if user.exists():
            RefreshToken.for_user(user.first()) #Lo que refresca es el access token
            return Response({'message': 'Sesion cerrada correctamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario'}, status=status.HTTP_400_BAD_REQUEST)





#
#CODIGO OBSOLETO - SIRVE PARA ESTUDIAR PERO NO LO APLICARE POR EL USO DE OTRAS HERRAMIENTAS
#
#
# class UserToken(APIView):
#     #clase para refrescar el token de un usuario
#     def get(self, request,*args, **kwargs):
#         username = request.GET.get('username')
#         try:
#             user_token = Token.objects.get(
#                 user =UserTokenSerializers().Meta.model.objects.filter(username = username).first()#validamos que el usuario exista
#             )
#             return Response({
#                 'token': user_token.key
#             })
#         except:
#             return Response({
#                 'error': 'Credenciales incorrectas'
#             }, status= status.HTTP_400_BAD_REQUEST)

# class Login(ObtainAuthToken): #Esta clase crea una vista normal y define el metodo post
#     def post(self, request, *args, **kwargs):
#         login_serializer = self.serializer_class(data=request.data, context = {'request':request})
#         #Esta clase ya la definio ObtainAuthToken, requiere el username y password, tambien token.
#         if login_serializer.is_valid():
#             user = login_serializer.validated_data['user']
#             if user.is_active:
#                 token,created = Token.objects.get_or_create(user = user)#Este metodo crea un token o lo llama si es que ya esta creado
#                 user_serializer = UserTokenSerializers(user)
#                 if created:
#                     return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Inicio de sesion correcto'}, status= status.HTTP_201_CREATED)
#                 else:
#                     all_sessions = Session.objects.filter(expire_date__gte = datetime.now()) #Hace que el sistema desloguee las sessiones que esten a la par de la que inicia sesion
#                     if all_sessions.exists():
#                         for session in all_sessions:
#                             session_data = session.get_decoded() #Si en alguna de las sessiones, se busca el usuario actual y lo encuentra, las borra
#                             if user.id == int(session_data.get('_auth_user_id')):
#                                 session.delete()
#                     token.delete()# Se borra el token, en caso de que vuelva a iniciar sesion
#                     token = Token.objects.create(user = user)#Se crea un token para validar las funciones
#                     return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Inicio de sesion correcto'}, status= status.HTTP_201_CREATED)
#             else:
#                 return Response({'error': 'usuario desactivado'}, status= status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({'error': 'Nombre o usuario incorrecto'}, status= status.HTTP_400_BAD_REQUEST)



# class Logout(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             token = request.GET.get('token')
#             token = Token.objects.filter(key = token).first()
#             if token:#Hacemos logout si el token del usuario es valido
#                 user = token.user
#                 all_sessions = Session.objects.filter(expire_date__gte = datetime.now()) #Hace que el sistema desloguee las sessiones que esten a la par de la que inicia sesion
#                 if all_sessions.exists():
#                     for session in all_sessions:
#                         session_data = session.get_decoded() #Si en alguna de las sessiones, se busca el usuario actual y lo encuentra, las borra
#                         if user.id == int(session_data.get('_auth_user_id')):
#                             session.delete()
#                 session_message = 'Sesiones de usuario eliminadas.'
#                 token.delete()
#                 token_message = 'Token eliminado'
#                 return Response({'token_message': token_message, 'session_message': session_message}, status = status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'No se encuentran usuario con estas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response({'error': 'no se ha encontrado token en la peticion'}, status=status.HTTP_409_CONFLICT)