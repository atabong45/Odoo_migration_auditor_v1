# auditor/report.py
from dataclasses import dataclass, asdict

@dataclass
class Issue:
    """
    Représente un seul problème de migration trouvé par un checker.
    """
    issue_code: str
    severity: str
    module_name: str
    file_path: str
    line_number: int
    description: str
    code_snippet: str

    def to_dict(self):
        """Convertit l'instance de dataclass en dictionnaire pour la sérialisation JSON."""
        return asdict(self)