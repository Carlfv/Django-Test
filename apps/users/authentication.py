from datetime import timedelta
from email import message
from django.utils import timezone
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed






class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False
    def expires_in(self, token): #Calcula el tiempo de expiracion
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token): #compara si el token esta expiradp
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token): #Obtenemos el valor de los calculos
        is_expired = self.is_token_expired(token)
        if is_expired:
            self.expired = True #Retornarla al final para que se le pueda enviar al front end y que sepa cuando refrescarlo si esta vencido
            token.delete()
            user = token.user
            #Podria borrarse tambien la session
            token = self.get_model().objects.create(user = user)#Si el token esta expirado, se elimina y se crea uno nuevo
        return is_expired, token

    #Autenticacion de token segun la libreria de DRF
    def authenticate_credentials(self, key):
        message, token, user = None, None, None
        try:
            token = self.get_model.objects.select_related('user').get(key=key)
            user = token.user
        except self.get_model.DoesNotExist:
            message = 'Token invalido'  
            self.expired = True
        if token is not None:
            if not token.user.is_active():
                message = 'usuario inactivo'

            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = 'Token Expirado'

        return (user, token, message,self.expired)
