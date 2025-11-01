import requests
import json
import sys

# --- CONFIGURATION ---
# REMPLACE CECI par l'URL de ton API. Si tu utilises le serveur de dev, c'est la bonne.
API_URL = "http://127.0.0.1:8000/api/submit-analysis/"

# REMPLACE CECI par la VRAIE clé d'API que tu as copiée depuis l'admin Django.
API_KEY = "3780a7f2-58c5-42e5-887a-8c74e383e645" # <--- METS TA CLÉ ICI !

# --- DONNÉES DE TEST ---
# C'est le payload que l'agent enverra.
# Note qu'il n'y a plus de "project_id".
test_payload = {
    "issues": [
        {
            "severity": "MAJOR",
            "module_name": "sale_custom",
            "file_path": "sale_custom/models/sale_order.py",
            "line_number": 42,
            "description": "Usage of deprecated @api.one decorator.",
            "code_snippet": "@api.one"
        },
        {
            "severity": "CRITICAL",
            "module_name": "account_extra",
            "file_path": "account_extra/models/account_move.py",
            "line_number": 101,
            "description": "Direct SQL query detected, this is risky for migrations.",
            "code_snippet": "self.env.cr.execute('SELECT * FROM sale_order')"
        }
    ]
}

# --- EXÉCUTION DE LA REQUÊTE ---

def run_test():
    if "3780a7f2-78c5-42e5-887a-8c74e383e645" in API_KEY:
        print("ERREUR : Tu n'as pas remplacé la clé d'API par défaut dans le script.")
        sys.exit(1)

    print(f"[*] Envoi du rapport d'analyse à {API_URL}")
    
    headers = {
        "Content-Type": "application/json",
        # C'est ici que la magie opère. L'en-tête doit être exactement comme ça.
        "Authorization": f"Api-Key {API_KEY}" 
    }

    try:
        response = requests.post(API_URL, data=json.dumps(test_payload), headers=headers)
        
        # Vérifie si la requête a réussi (code 2xx)
        response.raise_for_status()
        
        print("\n[SUCCÈS !] La requête a été acceptée (Code de statut :", response.status_code, ")")
        print("Réponse du serveur :")
        print(response.json())
        print("\nVa vérifier dans ton interface d'admin si la nouvelle 'AnalysisRun' a bien été créée !")

    except requests.exceptions.HTTPError as e:
        print("\n[ERREUR] La requête a échoué (Code de statut :", e.response.status_code, ")")
        print("Réponse du serveur :")
        try:
            print(e.response.json())
        except json.JSONDecodeError:
            print(e.response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\n[ERREUR] Impossible de contacter le serveur : {e}")

if __name__ == "__main__":
    run_test()