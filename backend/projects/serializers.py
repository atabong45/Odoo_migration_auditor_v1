# projects/serializers.py

from rest_framework import serializers
from .models import Project, AnalysisRun, Issue



class AnalysisRunListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisRun
        fields = ['id', 'status', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    analysis_runs = AnalysisRunListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        # On ne change que cette ligne
        fields = ['id', 'name', 'owner', 'git_url', 'api_key', 'created_at', 'analysis_runs']
        read_only_fields = ['owner']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'severity', 'module_name', 'file_path', 
            'line_number', 'description', 'code_snippet'
        ]


class AnalysisRunDetailSerializer(serializers.ModelSerializer):
    # C'est ici que la magie opère.
    # On déclare un champ 'issues' qui utilisera notre IssueSerializer.
    # many=True indique qu'il s'agit d'une liste de plusieurs objets.
    # read_only=True signifie que ce champ sera seulement lu, pas écrit via ce serializer.
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = AnalysisRun
        fields = [
            'id', 'project', 'status', 'created_at', 
            'completed_at', 'issues' 
        ]




class AnalysisRunCreateSerializer(serializers.ModelSerializer):
    # On redéfinit 'issues' pour qu'il soit inscriptible (writeable).
    # On utilise le 'slug' du serializer d'Issue que nous avons déjà, 
    # mais on enlève 'read_only=True'.
    issues = IssueSerializer(many=True)

    class Meta:
        model = AnalysisRun
        # On ne demande que le project_id et la liste des issues à l'agent.
        # Le statut et les dates seront gérés automatiquement.
        fields = [ 'issues']

    def create(self, validated_data):
        """
        On surcharge la méthode create pour gérer la création imbriquée.
        """
        # On extrait les données des 'issues' du dictionnaire validé.
        issues_data = validated_data.pop('issues')
        
        # On crée d'abord l'objet parent 'AnalysisRun'.
        # On passe directement le reste des données validées (ici, juste 'project').
        analysis_run = AnalysisRun.objects.create(**validated_data)
        
        # Ensuite, on boucle sur chaque 'issue' reçue...
        for issue_data in issues_data:
            # ...et on crée l'objet Issue en le liant à l'AnalysisRun parent.
            Issue.objects.create(analysis_run=analysis_run, **issue_data)
            
        return analysis_run