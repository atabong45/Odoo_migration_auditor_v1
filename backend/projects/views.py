from django.shortcuts import render
import uuid
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework.exceptions import PermissionDenied
from .models import Project, AnalysisRun
from .serializers import ProjectSerializer, AnalysisRunDetailSerializer,  AnalysisRunCreateSerializer
from .permissions import IsProjectOwner, IsAnalysisOwner, HasValidAPIKey

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
            """
            Associe automatiquement l'utilisateur connecté comme propriétaire du projet.
            """
            # request.user est l'utilisateur authentifié grâce au token.
            serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_path='latest-analysis')
    def latest_analysis(self, request, pk=None):
        """
        Endpoint personnalisé pour récupérer la dernière analyse d'un projet spécifique.
        URL générée : GET /api/projects/{pk}/latest-analysis/
        """
        # 1. On récupère le projet de manière sécurisée (vérifie que l'utilisateur est propriétaire)
        project = self.get_object()
        
        # 2. On cherche la dernière analyse liée à ce projet
        # .order_by('-created_at') trie de la plus récente à la plus ancienne
        # .first() prend la première de la liste (donc la plus récente)
        latest_run = project.analysis_runs.order_by('-created_at').first()

        # 3. Si aucune analyse n'existe, on renvoie une 404
        if not latest_run:
            return Response(
                {"detail": "Aucune analyse trouvée pour ce projet."}, 
                status=404
            )

        # 4. Sinon, on sérialise et on renvoie la réponse
        serializer = AnalysisRunDetailSerializer(latest_run)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='regenerate-api-key')
    def regenerate_api_key(self, request, pk=None):
        """
        Génère une nouvelle clé API pour le projet.
        """
        # self.get_object() garantit que seul le propriétaire peut accéder à cette action.
        project = self.get_object()
        
        # On génère une nouvelle clé UUID et on sauvegarde le projet.
        project.api_key = uuid.uuid4()
        project.save()
        
        # On renvoie une réponse avec la nouvelle clé.
        return Response({'api_key': project.api_key})
    

class AnalysisRunViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour lister et récupérer les détails des analyses.
    ReadOnlyModelViewSet ne permet que les opérations de lecture (pas de création/modif ici).
    """
    serializer_class = AnalysisRunDetailSerializer
    permission_classes = [IsAuthenticated, IsAnalysisOwner]

    def get_queryset(self):
        """
        On s'assure que l'utilisateur ne peut voir que les analyses
        des projets qui lui appartiennent.
        """
        return AnalysisRun.objects.filter(project__owner=self.request.user)


class AnalysisRunCreateView(generics.CreateAPIView):
    """
    Vue dédiée à la création d'une nouvelle analyse par l'agent CLI.
    """
    queryset = AnalysisRun.objects.all()
    serializer_class = AnalysisRunCreateSerializer
    permission_classes = [HasValidAPIKey]

    def perform_create(self, serializer):
        """
        Cette méthode est appelée juste avant de sauvegarder.
        Le projet est récupéré via la clé d'API grâce à notre permission
        et est disponible dans `self.request.project`.
        On le passe directement au serializer lors de la sauvegarde.
        """
        # La permission HasValidAPIKey a déjà validé la clé et stocké le projet ici.
        project = self.request.project
        
        # On passe le projet en argument additionnel à la méthode save().
        # Le serializer l'ajoutera à validated_data avant d'appeler sa méthode create().
        serializer.save(project=project)