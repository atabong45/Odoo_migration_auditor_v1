# auditor/checkers/base_checker.py
from abc import ABC, abstractmethod
from typing import List, Tuple
from ..report import Issue

class BaseChecker(ABC):
    """
    Classe de base abstraite pour tous les checkers.
    Chaque checker qui hérite de cette classe représente une règle d'analyse.
    """
    # --- Métadonnées pour l'évolutivité ---
    # Chaque checker DOIT définir un code unique.
    ISSUE_CODE: str = "GEN-000"
    
    # Sévérité par défaut, peut être surchargée.
    SEVERITY: str = "INFO"
    
    # Description du problème, peut contenir des placeholders comme {name}.
    DESCRIPTION: str = "No description provided."

    # Par défaut, une règle s'applique à toutes les versions.
    # Les checkers spécifiques surchargeront ces valeurs.
    APPLIES_FROM_VERSION: float = 0.0
    APPLIES_TO_VERSION: float = 99.0
    
    # Pour les règles très spécifiques à une migration (ex: 15.0 -> 16.0)
    APPLIES_ONLY_FOR_MIGRATION: Tuple[float, float] = None


    @abstractmethod
    def check(self, file_content: str, file_path: str, module_name: str) -> List[Issue]:
        """
        La méthode que chaque checker doit implémenter.
        Elle prend le contenu d'un fichier et retourne une liste de problèmes.
        """
        pass

class BasePythonChecker(BaseChecker):
    """
    Classe de base spécialisée pour les fichiers Python.
    Elle travaillera avec un Arbre Syntaxique Abstrait (AST) pour plus de robustesse.
    """
    @abstractmethod
    def check(self, ast_tree, file_path: str, module_name: str) -> List[Issue]:
        # Note: on change la signature. On ne prend plus le contenu brut,
        # mais un arbre AST déjà parsé, c'est beaucoup plus efficace.
        pass

class BaseXMLChecker(BaseChecker):
    """
    Classe de base spécialisée pour les fichiers XML.
    Elle travaillera avec un arbre XML parsé (lxml) pour des recherches efficaces.
    """
    @abstractmethod
    def check(self, xml_tree, file_path: str, module_name: str) -> List[Issue]:
        # Idem, on passe un arbre XML parsé.
        pass