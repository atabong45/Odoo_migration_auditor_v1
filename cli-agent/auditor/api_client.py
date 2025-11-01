# auditor/api_client.py
import requests
import json
import os
from dotenv import load_dotenv

# Cette ligne charge les variables du fichier .env dans l'environnement du script
load_dotenv()

# On récupère l'URL depuis les variables d'environnement.
# os.getenv() retournera None si la variable n'est pas trouvée.
SUBMIT_URL = os.getenv("AUDITOR_API_URL")

# C'est une sécurité importante : on s'assure que l'URL est bien configurée.
if not SUBMIT_URL:
    raise ValueError(
        "AUDITOR_API_URL is not set in your environment. "
        "Please create a .env file at the root of the cli-agent directory."
    )


def submit_report(report_data: dict, api_key: str):
    """
    Submits the analysis report to the backend API.

    Args:
        report_data: Un dictionnaire contenant les résultats de l'analyse (les "issues").
        api_key: La clé d'API du projet pour l'authentification.

    Returns:
        La réponse JSON du serveur en cas de succès.

    Raises:
        requests.exceptions.RequestException: Pour les erreurs de connexion ou les statuts HTTP d'erreur.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key}"
    }

    print(f"\nConnecting to {SUBMIT_URL} to submit the report...")

    try:
        response = requests.post(
            SUBMIT_URL,
            data=json.dumps(report_data),
            headers=headers,
            timeout=100
        )
        
        response.raise_for_status()
        
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error while submitting the report: {e}")
        
        if e.response is not None:
            print("Server response:", e.response.text)
        
        raise