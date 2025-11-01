# auditor/run.py
import ast
import json
import pkgutil
import importlib
import inspect
from tqdm import tqdm
from typing import List
from lxml import etree 

from . import discovery
from . import api_client
from .checkers.base_checker import BaseChecker, BasePythonChecker, BaseXMLChecker
from .report import Issue

def load_checkers(from_version: float, to_version: float) -> List[BaseChecker]:
    """
    Charge dynamiquement toutes les classes de checkers qui héritent de BaseChecker
    et les filtre pour ne garder que celles pertinentes pour la migration demandée.
    """
    checkers = []
    # On importe le package 'checkers'
    import auditor.checkers
    
    # On parcourt tous les modules à l'intérieur du package 'auditor.checkers'
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=auditor.checkers.__path__,
        prefix=auditor.checkers.__name__ + '.',
        onerror=lambda x: None
    ):
        module = importlib.import_module(modname)
        # On inspecte chaque membre du module
        for name, obj in inspect.getmembers(module):
            # On cherche les classes qui héritent de BaseChecker mais qui ne sont pas BaseChecker elles-mêmes
            if (inspect.isclass(obj) and issubclass(obj, BaseChecker) and obj not in [BaseChecker, BasePythonChecker, BaseXMLChecker]):
                # --- Logique de filtrage par version ---
                is_relevant = (
                    from_version >= obj.APPLIES_FROM_VERSION and
                    from_version <= obj.APPLIES_TO_VERSION
                )
                
                # On instancie la classe et on l'ajoute à la liste si elle est pertinente
                if is_relevant:
                    checkers.append(obj())
    
    return checkers

def start_audit(path: str, api_key: str, from_version: float, to_version: float, output_file: str = None):
    """
    Le point d'entrée principal de la logique d'audit.
    Orchestre la découverte, le chargement des règles, l'analyse et la soumission.
    """
    print("Step 1: Loading relevant audit rules...")
    checkers = load_checkers(from_version, to_version)
    if not checkers:
        print("No audit rules are relevant for this migration path. Exiting.")
        return
    
    python_checkers = [c for c in checkers if isinstance(c, BasePythonChecker)]
    xml_checkers = [c for c in checkers if isinstance(c, BaseXMLChecker)] 

    print(f"Loaded {len(checkers)} rules ({len(python_checkers)} for Python), {len(xml_checkers)} for XML).")

    print("\nStep 2: Discovering Odoo modules and files...")
    all_files = discovery.find_odoo_modules(path)
    print(f"Found {len(all_files)} files to analyze.")

    all_issues: List[Issue] = []
    print("\nStep 3: Analyzing files...")
    
    # On utilise tqdm pour créer une barre de progression
    for module_name, file_path, relative_path in tqdm(all_files, desc="Scanning files"):
         # LOGIQUE POUR PYTHON 
        if file_path.endswith(".py") and python_checkers:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # On parse le fichier en AST une seule fois
                    ast_tree = ast.parse(content, filename=file_path)
                    
                    # On passe l'arbre à tous les checkers Python pertinents
                    for checker in python_checkers:
                        found_issues = checker.check(ast_tree, relative_path, module_name)
                        all_issues.extend(found_issues)
            except (SyntaxError, UnicodeDecodeError) as e:
                tqdm.write(f"Warning: Skipping file {file_path} due to parsing error: {e}")
            except Exception as e:
                tqdm.write(f"Warning: An unexpected error occurred with file {file_path}: {e}")
            
        # LOGIQUE POUR XML
        elif file_path.endswith(".xml") and xml_checkers:
            try:
                # On parse le fichier XML avec lxml. `recover=True` évite de planter sur un XML mal formé.
                xml_tree = etree.parse(file_path, parser=etree.XMLParser(recover=True))
                
                # On passe l'arbre XML à tous les checkers XML pertinents
                for checker in xml_checkers:
                    found_issues = checker.check(xml_tree, relative_path, module_name)
                    all_issues.extend(found_issues)
            except etree.XMLSyntaxError as e:
                tqdm.write(f"Warning: Skipping file {file_path} due to XML syntax error: {e}")
            except Exception as e:
                tqdm.write(f"Warning: An unexpected error occurred with file {file_path}: {e}")

    print(f"\nStep 4: Analysis complete. Found {len(all_issues)} total issues.")

    if not all_issues:
        print("No issues found. Nothing to submit.")
        return

    # On convertit notre liste d'objets Issue en une liste de dictionnaires
    report_data = {
        "issues": [issue.to_dict() for issue in all_issues]
    }
    
    if output_file:
        print(f"\nSaving report to {output_file}...")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=4)
        except IOError as e:
            # On utilise tqdm.write pour ne pas casser la barre de progression si elle est active
            tqdm.write(f"Error: Could not write to file {output_file}: {e}")
            raise # On propage l'erreur pour que main.py l'attrape
    else:
        # C'est le comportement précédent
        api_client.submit_report(report_data, api_key)