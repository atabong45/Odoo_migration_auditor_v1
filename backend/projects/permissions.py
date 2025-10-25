# projects/permissions.py

from rest_framework.permissions import BasePermission

class IsProjectOwner(BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les propriétaires d'un projet.
    """
    def has_object_permission(self, request, view, obj):
        # 'obj' ici est l'instance du projet.
        # On vérifie si le propriétaire de l'objet est l'utilisateur qui fait la requête.
        return obj.owner == request.user

class IsAnalysisOwner(BasePermission):
    """
    Permission personnalisée pour les objets liés à un projet (comme AnalysisRun).
    """
    def has_object_permission(self, request, view, obj):
        # 'obj' ici est l'instance de l'AnalysisRun.
        # On vérifie via la relation ForeignKey.
        return obj.project.owner == request.user