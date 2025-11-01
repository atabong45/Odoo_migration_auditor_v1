# Odoo Migration Auditor - Backend API

Ce dossier contient le code source de l'API REST du projet Odoo Migration Auditor.

Cette API est construite avec **Django** et **Django Rest Framework** et est responsable de la gestion des utilisateurs, des projets, des analyses, ainsi que de l'authentification et des permissions.

## ⚙️ Stack Technique

- **Framework :** Django
- **API :** Django Rest Framework
- **Authentification :** JWT (via `djangorestframework-simplejwt`)
- **Base de données (Développement) :** SQLite
- **Base de données (Production) :** PostgreSQL (prévu)
- **Gestion des CORS :** `django-cors-headers`

## Endpoints Principaux

- `/api/auth/register/` : Création d'un nouvel utilisateur.
- `/api/token/` : Obtention des tokens JWT (connexion).
- `/api/token/refresh/` : Rafraîchissement du token d'accès.
- `/api/auth/me/` : Récupération des informations de l'utilisateur connecté.
- `/api/projects/` : Liste et création des projets.
- `/api/projects/{id}/latest-analysis/` : Récupération de la dernière analyse d'un projet.
- `/api/submit-analysis/` : Soumission d'un rapport d'analyse complet par l'agent CLI.

---

## 🚀 Guide d'Installation (Développement Local)

### 1. Prérequis

- Python (version 3.10 ou supérieure recommandée).
- Un gestionnaire d'environnement comme `venv` ou `conda`.

### 2. Installation

1.  **Naviguez dans le dossier du backend :**

    ```bash
    cd backend
    ```

2.  **Créez et activez un environnement virtuel.**

    _Avec `conda` (méthode recommandée pour ce projet) :_

    ```bash
    conda create --name odoo-auditor-backend python=3.10 -y
    conda activate odoo-auditor-backend
    ```

    _Ou avec `venv` :_

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    ```

3.  **Installez les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration de la Base de Données

1.  **Créez les migrations :** Django va inspecter vos modèles et préparer les changements pour la base de données.

    ```bash
    python manage.py makemigrations
    ```

2.  **Appliquez les migrations :** Cette commande va créer le fichier `db.sqlite3` (s'il n'existe pas) et y construire toutes les tables nécessaires.

    ```bash
    python manage.py migrate
    ```

3.  **Créez un super-utilisateur** pour accéder à l'interface d'administration :
    ```bash
    python manage.py createsuperuser
    ```
    Suivez les instructions pour définir un nom d'utilisateur et un mot de passe.

### 4. Lancement du Serveur

1.  **Démarrez le serveur de développement Django :**

    ```bash
    python manage.py runserver
    ```

2.  Le serveur est maintenant en écoute. Vous pouvez y accéder :
    - **Interface d'administration :** `http://127.0.0.1:8000/admin/`
    - **Browsable API :** `http://127.0.0.1:8000/api/`

---
