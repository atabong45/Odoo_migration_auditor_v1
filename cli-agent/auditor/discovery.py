# auditor/discovery.py
import os
from typing import List, Tuple

def find_odoo_modules(project_path: str) -> List[Tuple[str, str, str]]:
    """
    Parcourt un répertoire, identifie les modules Odoo et liste leurs fichiers.

    Args:
        project_path: Le chemin du répertoire des addons à analyser.

    Returns:
        Une liste de tuples. Chaque tuple contient:
        (nom_du_module, chemin_complet_du_fichier, chemin_relatif_du_fichier)
    """
    all_files = []
    
    for root, dirs, files in os.walk(project_path):
        # Si on trouve un manifest, on sait qu'on est à la racine d'un module.
        if '__manifest__.py' in files:
            module_name = os.path.basename(root)
            print(f"  -> Discovered module: {module_name}")
            
            # On parcourt à nouveau ce dossier de module pour lister tous ses fichiers.
            for sub_root, _, sub_files in os.walk(root):
                for file_name in sub_files:
                    # On ignore les fichiers cachés ou les fichiers de cache
                    if file_name.startswith('.') or '__pycache__' in sub_root:
                        continue
                        
                    file_path = os.path.join(sub_root, file_name)
                    relative_path = os.path.relpath(file_path, project_path)
                    all_files.append((module_name, file_path, relative_path))
            
            # On empêche os.walk de descendre dans les sous-dossiers qui 
            # pourraient aussi être des modules (cas rare mais possible).
            dirs[:] = [] 

    return all_files