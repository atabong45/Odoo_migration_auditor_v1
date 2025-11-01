# auditor/checkers/python_checkers.py
import ast
from typing import List
from .base_checker import BasePythonChecker
from ..report import Issue

class DeprecatedApiOneChecker(BasePythonChecker):
    """
    Cette règle détecte l'utilisation du décorateur @api.one, qui est déprécié.
    Elle analyse l'arbre syntaxique pour trouver les décorateurs sur les fonctions.
    """
    # --- Métadonnées de la règle ---
    ISSUE_CODE = "PY001"
    SEVERITY = "MAJOR"
    DESCRIPTION = "Usage of deprecated @api.one decorator. It should be replaced with a loop over 'self'."
    
    # Cette règle concerne du code qui était valide avant, mais qui doit être changé
    # pour la v17. On considère qu'elle est pertinente pour toute migration vers une version >= 13.
    APPLIES_FROM_VERSION = 8.0
    APPLIES_TO_VERSION = 16.0 # Le problème existe jusqu'à la v16 incluse.

    def check(self, ast_tree, file_path: str, module_name: str) -> List[Issue]:
        issues = []
        # ast.walk parcourt tous les nœuds de l'arbre syntaxique.
        for node in ast.walk(ast_tree):
            # On s'intéresse uniquement aux nœuds qui sont des définitions de fonctions.
            if isinstance(node, ast.FunctionDef):
                # On inspecte la liste des décorateurs de cette fonction.
                for decorator in node.decorator_list:
                    # On vérifie si le décorateur est bien de la forme `api.one`
                    is_api_one = (
                        isinstance(decorator, ast.Attribute) and
                        isinstance(decorator.value, ast.Name) and
                        decorator.value.id == 'api' and
                        decorator.attr == 'one'
                    )
                    
                    if is_api_one:
                        # Si on trouve le décorateur, on crée un "Issue"
                        new_issue = Issue(
                            issue_code=self.ISSUE_CODE,
                            severity=self.SEVERITY,
                            module_name=module_name,
                            file_path=file_path,
                            line_number=decorator.lineno, # L'AST nous donne le numéro de ligne !
                            description=self.DESCRIPTION,
                            code_snippet=f"@{ast.unparse(decorator)}" # Recrée le code du décorateur
                        )
                        issues.append(new_issue)
        return issues
    

class DirectSQLChecker(BasePythonChecker):
    """
    Cette règle détecte l'utilisation de requêtes SQL directes via
    `self.env.cr.execute` ou `self._cr.execute`, ce qui est une
    mauvaise pratique et un risque majeur pour les migrations.
    """
    # --- Métadonnées de la règle ---
    ISSUE_CODE = "PY002"
    SEVERITY = "CRITICAL" # C'est un problème très grave.
    DESCRIPTION = (
        "Direct SQL query detected. This is a major risk for migrations "
        "as database schema can change. Use ORM methods instead."
    )

    # Ce problème est pertinent pour toutes les versions.
    APPLIES_FROM_VERSION = 8.0
    APPLIES_TO_VERSION = 99.0 # Toujours pertinent.

    def check(self, ast_tree, file_path: str, module_name: str) -> List[Issue]:
        issues = []
        # On parcourt à nouveau l'arbre à la recherche de nœuds spécifiques.
        # Ici, on cherche des "appels de fonction" (Call).
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Call):
                # On veut vérifier si la fonction appelée est 'execute'.
                # La structure d'un appel est : `func(...)`.
                # `node.func` représente la partie `func`.
                
                # On s'assure que `node.func` est un attribut (comme dans `objet.methode`)
                if not isinstance(node.func, ast.Attribute):
                    continue

                # On vérifie si le nom de l'attribut (la méthode) est bien 'execute'.
                if node.func.attr == 'execute':
                    # Maintenant on doit vérifier l'objet de gauche.
                    # La structure est `value.attr`.
                    # Ex: `self.env.cr`. Ici, `value` est `self.env` et `attr` est `cr`.
                    
                    # Cas 1: `self._cr.execute`
                    # `node.func.value` représente `self._cr`
                    is_self_cr = (
                        isinstance(node.func.value, ast.Attribute) and
                        node.func.value.attr == '_cr' and
                        isinstance(node.func.value.value, ast.Name) and
                        node.func.value.value.id == 'self'
                    )

                    # Cas 2: `self.env.cr.execute`
                    # C'est une cascade d'attributs. `node.func.value` représente `self.env.cr`
                    is_self_env_cr = (
                        isinstance(node.func.value, ast.Attribute) and
                        node.func.value.attr == 'cr' and
                        isinstance(node.func.value.value, ast.Attribute) and
                        node.func.value.value.attr == 'env' and
                        isinstance(node.func.value.value.value, ast.Name) and
                        node.func.value.value.value.id == 'self'
                    )

                    if is_self_cr or is_self_env_cr:
                        new_issue = Issue(
                            issue_code=self.ISSUE_CODE,
                            severity=self.SEVERITY,
                            module_name=module_name,
                            file_path=file_path,
                            line_number=node.lineno,
                            description=self.DESCRIPTION,
                            code_snippet=ast.unparse(node).strip() # On affiche toute la ligne de l'appel
                        )
                        issues.append(new_issue)
                        
        return issues
    

