# projects/serializers.py

from rest_framework import serializers
from .models import Project

# On crée une classe qui hérite de ModelSerializer de DRF.
class ProjectSerializer(serializers.ModelSerializer):
    
    # La sous-classe Meta est utilisée pour configurer le serializer.
    class Meta:
        model = Project  # On lui dit quel modèle il doit transformer.
        
        # On liste les champs du modèle qu'on veut inclure dans le JSON.
        fields = ['id', 'name', 'owner', 'api_key', 'created_at']