from django.contrib import admin

# Register your models here.
# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# On définit une classe pour personnaliser l'affichage de notre CustomUser dans l'admin.
# En héritant de UserAdmin, on récupère toutes les fonctionnalités de base de Django
# (gestion des mots de passe, permissions, etc.).
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Si plus tard tu ajoutes des champs à CustomUser (ex: 'company_name'),
    # tu pourras les afficher ici dans des listes ou des formulaires.
    # Pour l'instant, on ne fait rien de plus.

# On "enregistre" notre modèle CustomUser auprès du site d'administration,
# en lui disant d'utiliser la classe de configuration CustomUserAdmin.
admin.site.register(CustomUser, CustomUserAdmin)