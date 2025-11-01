# projects/permissions.py
from .models import Project, AnalysisRun
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
    

class HasValidAPIKey(BasePermission):
    """
    Permission qui vérifie la présence et la validité d'une clé d'API
    dans les en-têtes de la requête.
    """
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        # On cherche la clé dans l'en-tête 'Authorization', au format "Api-Key <votre_clé>"
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Api-Key '):
            return False

        # On extrait la clé elle-même
        api_key = auth_header.split(' ')[1]

        try:
            # On cherche si un projet correspond à cette clé
            project = Project.objects.get(api_key=api_key)
            
            # C'est l'astuce : on attache le projet trouvé directement à l'objet 'request'.
            # Ça nous évitera de le chercher à nouveau dans la vue.
            request.project = project
            return True
        except Project.DoesNotExist:
            return False