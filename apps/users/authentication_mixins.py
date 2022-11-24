# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
# from rest_framework.authentication import get_authorization_header
# from apps.users.authentication import ExpiringTokenAuthentication

# class Authentication(object):

# #usamos el get autorizathion header para que se proceda a la validacion del sistema completo

#     user = None
#     user_token_expired = False
#     #Llamar al token de usuario que mande la solciitud
#     def get_user(self, request):
#         token = get_authorization_header(request).split()
#         if token:
#             try:
#                 token = token[1].decode()
#             except:
#                 return None
#             token_expire =ExpiringTokenAuthentication()
#             user, token, message, expired = token_expire.authenticate_credentials(token)#Autenticamos el token con Expiring   
#             if user != None and token!= None:
#                 self.user = user
#                 return user
#             return message
#         return None

#     def dispatch(self, request, *args, **kwargs):
#         user = self.get_user(request)
#         if user is not None:#Encontro un token en la peticion
#             if type(user) == str:
#                 response = Response({'error': user,'expired': self.user_token_expired}, status= status.HTTP_401_UNAUTHORIZED) #Le indicamos al front end cuando expiro el token 
#                 response.accepted_renderer = JSONRenderer()
#                 response.accepted_media_type = 'application/json'
#                 response.rendered_context = {}
#                 return response
#             if not self.user_token_expired:
#                 return super().dispatch(request, *args, **kwargs)
#         #Esto se hace en los casos que un response se use en una clase que no herede DRF
#         response = Response({'error': 'No se han enviado las credenciales','expired': self.user_token_expired}, status=status.HTTP_400_BAD_REQUEST)
#         response.accepted_renderer = JSONRenderer()
#         response.accepted_media_type = 'application/json'
#         response.rendered_context = {}
#         return response
