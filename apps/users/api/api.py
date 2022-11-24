from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from apps.users.authentication_mixins import Authentication
from rest_framework import viewsets
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, UserListSerializers, UpdateUserSerializer
from rest_framework import status

#Las API views tambien podrian ser visualizadas como classes, 
#pero con el uso de decorators se permite trabajar como funciones, siempre y cuando se le definan los metodos

class UserViewSet(viewsets.GenericViewSet): #No esta basado en un modelo, lo que tiene incorporado es que hereda GenericApiView
    #Obtiene los metodos en especifico getobject y getqueryset
    #No tiene accion predeterminado pero permite implementar como por ejemplo en un viewSet Normal
    #Al ser genericos solo genera las rutas cuando los metodos sean definidos explicitamente
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializers
    update_serializer_class = UpdateUserSerializer
    queryset = None 

    def get_object(self, pk): #Funcion para buscar un usuario en la BD o retornar error
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset =  self.serializer_class().Meta.model.objects\
                            .filter(is_active=True)\
                            .values('id', 'email', 'name') #Nos trae los usuarios activos del sistema con el queryset
        return self.queryset

    def list(self, request): #Listado de usuario
        users = self.get_queryset()
        users_serializers = self.list_serializer_class(users, many = True) #many porque son varios, en caso de
        return Response(users_serializers.data, status=status.HTTP_200_OK)


    def create(self, request): #Creacion de usuario
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario registrado'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Error en el registro',
            'errors': user_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None): #Detalle de un usuario
        user  = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data, status= status.HTTP_200_OK)

    def update(self, request, pk=None):#Actualizar usuario
        user = self.get_object(pk)
        user_serializer =self.update_serializer_class(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario Actualizado'
            }, status=status.HTTP_200_OK)
        return Response({
            'message':'Error en la actualizacion',
            'errors': user_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        user_destroy =self.model.objects.filter(id = pk).update(is_active=False)
        if user_destroy==1:
            return Response({
                'message': 'Usuario Eliminado'
            }, status=status.HTTP_200_OK)
        return Response({
            'message':'No existe ese usuario'
            
        }, status= status.HTTP_404_NOT_FOUND)