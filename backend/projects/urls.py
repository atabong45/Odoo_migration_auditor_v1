# projects/urls.py
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
# On enregistre notre ViewSet auprès du routeur.
# 'projects' sera la base de l'URL (ex: /api/projects/)
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = router.urls