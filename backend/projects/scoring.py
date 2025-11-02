SEVERITY_COSTS = {
    'CRITICAL': 5.0,
    'MAJOR': 2.0,
    'MINOR': 0.5,
    'INFO': 0.1,
}

ISSUE_CODE_OVERRIDE_COSTS = {
    # Une requête SQL est pire qu'un CRITICAL standard
    'PY002': 8.0, 
    
    # track_visibility est un MINOR, mais il est vraiment très simple à corriger
    'XML001': 0.1, 
}

def calculate_effort_score(issues) -> float:
    """
    Calcule un score d'effort total pour une liste d'objets Issue.
    
    La logique est :
    1. Chercher un coût d'override spécifique pour le code de l'issue.
    2. Si non trouvé, utiliser le coût par défaut de la sévérité de l'issue.
    """
    total_score = 0.0
    for issue in issues:
        # On utilise .get() pour éviter une erreur si la clé n'existe pas
        cost = ISSUE_CODE_OVERRIDE_COSTS.get(
            issue.issue_code,  # La clé à chercher (ex: 'PY002')
            SEVERITY_COSTS.get(issue.severity, 0.0) # La valeur par défaut si la clé n'est pas trouvée
        )
        total_score += cost
        
    return total_score