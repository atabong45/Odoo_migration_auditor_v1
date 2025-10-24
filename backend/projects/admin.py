from django.contrib import admin

# Register your models here.
# projects/admin.py

from django.contrib import admin
from .models import Project, AnalysisRun

# Pour ces modèles, on n'a pas besoin de configuration complexe pour l'instant.
# On les enregistre simplement. Django leur créera une interface par défaut.
admin.site.register(Project)
admin.site.register(AnalysisRun)