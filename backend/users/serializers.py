# users/serializers.py

from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # On ajoute une confirmation de mot de passe qui ne sera pas stockée en BDD.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        # On définit les champs que notre API attendra pour une inscription.
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True} # Le mot de passe ne sera jamais renvoyé par l'API.
        }

    def validate(self, data):
        """
        Cette méthode est appelée pour valider les données reçues.
        On vérifie ici que les deux mots de passe correspondent.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return data

    def create(self, validated_data):
        """
        Cette méthode est appelée pour créer le nouvel utilisateur.
        On surcharge la méthode create pour gérer le hashage du mot de passe.
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # On ne permet de changer que l'email et le nom d'utilisateur (qui sert de nom complet ici)
        fields = ['username', 'email']


# NOUVEAU : Serializer pour le changement de mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Votre ancien mot de passe est incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError("Le nouveau mot de passe doit être différent de l'ancien.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user