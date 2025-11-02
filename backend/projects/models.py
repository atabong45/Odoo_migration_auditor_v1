from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    git_url = models.URLField(max_length=200, blank=True, null=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class AnalysisRun(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'Running'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='analysis_runs')
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    effort_score = models.FloatField(default=0.0, help_text="Score d'effort calculé basé sur les issues trouvées.")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Analysis for {self.project.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Issue(models.Model):
    class SeverityChoices(models.TextChoices):
        CRITICAL = 'CRITICAL', 'Critical'
        MAJOR = 'MAJOR', 'Major'
        MINOR = 'MINOR', 'Minor'
        INFO = 'INFO', 'Info'

    analysis_run = models.ForeignKey(
        AnalysisRun,
        on_delete=models.CASCADE,
        related_name='issues'
    )
    severity = models.CharField(
        max_length=10,
        choices=SeverityChoices.choices,
        default=SeverityChoices.INFO
    )
    module_name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=255)
    line_number = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    code_snippet = models.TextField(blank=True)
    issue_code = models.CharField(max_length=20, blank=True, null=True, help_text="Code unique identifiant le type de problème")
    
    def __str__(self):
        return f"{self.severity} in {self.file_path} (L{self.line_number})"