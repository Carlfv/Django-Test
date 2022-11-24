from django.contrib import admin
from django.urls import path, include
from apps.users.views import Login, Logout

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #Retorna el token de acceso y el refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #Refresca el token que se está usando
    path('login/', Login.as_view(), name = 'Login'),
    path('logout/', Logout.as_view(), name = 'Login'),
    path('usuario/', include('apps.users.api.routers')),
    #path('refresh-token/', UserToken.as_view(), name='refresh_token')
]
