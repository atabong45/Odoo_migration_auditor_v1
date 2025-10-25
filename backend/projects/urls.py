# projects/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AnalysisRunViewSet, AnalysisRunCreateView

router = DefaultRouter()
# On enregistre notre ViewSet auprès du routeur.
# 'projects' sera la base de l'URL (ex: /api/projects/)
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'analyses', AnalysisRunViewSet, basename='analysis')
urlpatterns = router.urls

urlpatterns = router.urls + [
    # Cette ligne définit l'URL pour la soumission d'analyse.
    path('submit-analysis/', AnalysisRunCreateView.as_view(), name='submit-analysis'),
]