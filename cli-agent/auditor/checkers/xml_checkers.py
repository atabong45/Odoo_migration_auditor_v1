# auditor/checkers/xml_checkers.py
from lxml import etree
from typing import List
from .base_checker import BaseXMLChecker
from ..report import Issue

class TrackVisibilityChecker(BaseXMLChecker):
    """
    Cette règle détecte l'utilisation de l'attribut déprécié `track_visibility`
    sur les balises <field> dans les vues XML.
    """
    # --- Métadonnées de la règle ---
    ISSUE_CODE = "XML001"
    SEVERITY = "MINOR" # C'est un changement simple à faire.
    DESCRIPTION = (
        "The attribute 'track_visibility' is deprecated. "
        "It should be replaced by the 'tracking' attribute on the model field definition in Python."
    )

    # Le changement a eu lieu en v13.
    APPLIES_FROM_VERSION = 8.0
    APPLIES_TO_VERSION = 16.0 # Pertinent pour les projets jusqu'à la v16.

    def check(self, xml_tree, file_path: str, module_name: str) -> List[Issue]:
        issues = []
        
        # On utilise XPath, un langage de requête pour XML.
        # Cette requête cherche toutes les balises <field> qui ont un attribut 'track_visibility'.
        # `//` signifie "cherche n'importe où dans le document".
        # `[@track_visibility]` est la condition sur l'attribut.
        nodes_with_issue = xml_tree.xpath("//field[@track_visibility]")

        for node in nodes_with_issue:
            new_issue = Issue(
                issue_code=self.ISSUE_CODE,
                severity=self.SEVERITY,
                module_name=module_name,
                file_path=file_path,
                line_number=node.sourceline, # lxml nous donne le numéro de ligne !
                description=self.DESCRIPTION,
                code_snippet=etree.tostring(node, pretty_print=False).decode('utf-8').strip()
            )
            issues.append(new_issue)
            
        return issues