from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('projects.urls')),
    # NOUVELLES URLs pour l'authentification
    path('api/auth/', include('users.urls')), # Pour notre vue d'inscription
    
    # URLs fournies par simplejwt pour la connexion et le rafraîchissement du token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

