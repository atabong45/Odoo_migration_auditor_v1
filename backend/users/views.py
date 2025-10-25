from django.shortcuts import render

# Create your views here.
# users/views.py

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer, UserProfileSerializer, ChangePasswordSerializer
from rest_framework.views import APIView

# generics.CreateAPIView est une vue pré-construite par DRF
# qui est spécialisée dans la création d'objets.
class UserCreateView(generics.CreateAPIView):
    """
    Vue pour créer un nouvel utilisateur. Accessible à tout le monde.
    """
    queryset = CustomUser.objects.all()
    
    # On spécifie que n'importe qui (même non authentifié) peut accéder à cette vue.
    permission_classes = [AllowAny]
    
    # On connecte cette vue à notre serializer.
    serializer_class = UserSerializer


    # NOUVELLE VUE CI-DESSOUS
class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Vue pour mettre à jour le profil de l'utilisateur connecté.
    Accepte les requêtes PATCH.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # On s'assure que l'utilisateur ne peut mettre à jour que son propre profil
        return self.request.user


# NOUVELLE VUE CI-DESSOUS
class ChangePasswordView(generics.UpdateAPIView):
    """
    Vue pour changer le mot de passe de l'utilisateur connecté.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "Mot de passe changé avec succès."}, status=status.HTTP_200_OK)
        
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Renvoie les données de l'utilisateur actuellement authentifié.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)