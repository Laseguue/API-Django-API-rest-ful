# API Django - API Restful

## Description
API Django - API Restful est une application web Django qui expose une API Restful. Cette application permet de gérer des projets, des utilisateurs, et d'autres entités à travers des endpoints API.

## Fonctionnalités
- Gestion des utilisateurs : inscription, authentification, et gestion des profils.
- Gestion des projets : création, modification, et suppression des projets.
- Gestion des issues : création, modification, et suppression des issues associées à un projet.
- Gestion des commentaires : ajout de commentaires aux issues.

## Structure du Projet
- `softdesk/api` : Dossier contenant les fichiers de l'API, tels que les modèles, les vues, et les serializers.
- `softdesk/softdesk` : Dossier contenant les fichiers de configuration de l'application Django.
- `venv` : Dossier contenant l'environnement virtuel Python.

## Exigences
- Python 3.x
- Django 3.x
- Django Rest Framework

## Installation
1. Clonez le dépôt GitHub.
2. Naviguez vers le dossier du projet.
3. Créez et activez un environnement virtuel Python.
4. Installez les dépendances avec `pip install -r requirements.txt` (si un fichier requirements.txt est présent).
5. Exécutez les migrations avec `python manage.py migrate`.
6. Démarrez le serveur de développement avec `python manage.py runserver`.
7. Accédez à l'API via `http://127.0.0.1:8000/api/`.

## Utilisation
Utilisez les endpoints API pour gérer les utilisateurs, les projets, les issues, et les commentaires. Consultez la documentation de l'API pour plus d'informations sur les endpoints disponibles et les méthodes HTTP supportées.

## Auteur
[Laseguue](https://github.com/Laseguue)
