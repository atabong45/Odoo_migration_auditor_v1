# Odoo Migration Auditor

**Odoo Migration Auditor** est une plateforme SaaS conçue pour aider les développeurs et les entreprises à planifier et à exécuter la migration de leurs applications Odoo. L'outil fournit une analyse statique de code approfondie pour identifier les incompatibilités, estimer la charge de travail et générer une feuille de route claire pour la migration.

## ✨ Philosophie du Projet

La migration d'un ERP est une opération critique, coûteuse et souvent sous-estimée. Ce projet vise à remplacer l'incertitude par la **visibilité** et la **prédictibilité**, en fournissant des données concrètes avant même le début du développement.

## 🏛️ Architecture Globale

Le projet est divisé en trois composants principaux :

1.  **[Frontend](./frontend/README.md)** : Une application web moderne et réactive (React, Vite, TypeScript, Tailwind CSS) qui sert de tableau de bord pour visualiser les projets, les résultats d'analyse et gérer son compte.
2.  **[Backend](./backend/README.md)** : Une API REST robuste (Django, Django Rest Framework) qui gère l'authentification, le stockage des données des projets et des analyses.
3.  **[Agent CLI](./agent-cli/)** : Un outil en ligne de commande (Python) qui effectue l'analyse statique du code Odoo localement et envoie les résultats au backend. (En cours de développement)

Chaque composant a son propre `README` détaillé pour les instructions d'installation et de développement.

## 🚀 Démarrage Rapide (Environnement Complet)

Ce projet est conçu pour être lancé avec Docker pour une mise en place simplifiée de l'environnement de développement.

_(Note : La configuration Docker sera ajoutée ultérieurement. Pour l'instant, veuillez suivre les guides d'installation individuels pour le [backend](./backend/README.md) et le [frontend](./frontend/README.md).)_

## 🗺️ Feuille de Route (V1)

- [x] **Backend :** API pour l'authentification, la gestion des projets et la soumission d'analyses.
- [x] **Frontend :** Interface utilisateur pour l'inscription, la connexion, l'affichage des projets et des résultats d'analyse.
- [ ] **Agent CLI :** Développement de l'outil d'analyse de code pour la migration Odoo 16 -> 17.
- [ ] **Déploiement :** Dockerisation complète et mise en place d'un environnement de production.

---
