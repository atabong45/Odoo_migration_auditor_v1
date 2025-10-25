# Odoo Migration Auditor - Backend

Ce dépôt contient le code source du backend pour le projet Odoo Migration Auditor. Il s'agit d'une API REST construite avec Django et Django Rest Framework, conçue pour recevoir et stocker les résultats d'analyse de l'agent d'audit.

## Fonctionnalités Principales (V1)

- Gestion des utilisateurs et authentification par tokens JWT.
- Gestion de Projets et de leurs Analyses (Analysis Runs).
- API sécurisée pour soumettre et récupérer les données d'audit.
- Interface d'administration Django pour une gestion facile des données.

## Stack Technique

- **Langage :** Python 3.10+
- **Framework :** Django
- **API :** Django Rest Framework
- **Authentification :** Simple JWT
- **Base de données (développement) :** SQLite

---

## Guide d'Installation et de Lancement

Suivez ces étapes pour mettre en place un environnement de développement local.

### 1. Prérequis

- Python 3.10 ou supérieur
- Un gestionnaire d'environnement comme `venv` ou `conda` (recommandé)

### 2. Installation

1.  **Clonez le dépôt :**

    ```bash
    git clone [URL_DE_VOTRE_DEPOT_GITHUB]
    cd backend
    ```

2.  **Créez et activez un environnement virtuel :**
    _Avec venv :_

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    ```

    _Avec conda :_

    ```bash
    conda create --name odoo-auditor-backend python=3.10 -y
    conda activate odoo-auditor-backend
    ```

3.  **Installez les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration Initiale

1.  **Appliquez les migrations de la base de données :**

    ```bash
    python manage.py migrate
    ```

2.  **Créez un super-utilisateur** pour accéder à l'interface d'administration :
    ```bash
    python manage.py createsuperuser
    ```
    Suivez les instructions pour définir un nom d'utilisateur et un mot de passe.

### 4. Lancement

1.  **Démarrez le serveur de développement :**

    ```bash
    python manage.py runserver
    ```

2.  Le backend est maintenant accessible :
    - **API :** `http://127.0.0.1:8000/api/`
    - **Interface d'administration :** `http://127.0.0.1:8000/admin/`

---
