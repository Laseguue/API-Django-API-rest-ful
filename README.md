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
Authentification
Token d'authentification :

Endpoint : /token-auth/
Méthode HTTP : POST
Données requises : username, password
Réponse : Token JWT pour l'authentification.
Rafraîchissement du token :

Endpoint : /token-refresh/
Méthode HTTP : POST
Données requises : Token JWT actuel.
Réponse : Nouveau token JWT.
Utilisateurs
Lister et créer des utilisateurs :

Endpoint : /users/
Méthode HTTP : GET (pour lister), POST (pour créer)
Données requises pour la création : username, password, age, etc.
Récupérer, mettre à jour ou supprimer un utilisateur :

Endpoint : /users/<int:pk>/
Méthode HTTP : GET, PUT, DELETE
Projets
Lister et créer des projets :
Endpoint : /projects/
Méthode HTTP : GET (pour lister), POST (pour créer)
Récupérer, mettre à jour ou supprimer un projet :
Endpoint : /projects/<int:pk>/
Méthode HTTP : GET, PUT, DELETE
Issues
Lister et créer des issues :
Endpoint : /issues/
Méthode HTTP : GET (pour lister), POST (pour créer)
Récupérer, mettre à jour ou supprimer une issue :
Endpoint : /issues/<int:pk>/
Méthode HTTP : GET, PUT, DELETE
Commentaires
Lister et créer des commentaires :
Endpoint : /comments/
Méthode HTTP : GET (pour lister), POST (pour créer)
Récupérer, mettre à jour ou supprimer un commentaire :
Endpoint : /comments/<uuid:pk>/
Méthode HTTP : GET, PUT, DELETE
Contributeurs
Lister et créer des contributeurs :
Endpoint : /contributors/
Méthode HTTP : GET (pour lister), POST (pour créer)
Récupérer, mettre à jour ou supprimer un contributeur :
Endpoint : /contributors/<int:pk>/
Méthode HTTP : GET, PUT, DELETE

Remarque : Assurez-vous d'avoir un token d'authentification valide pour accéder à la plupart de ces endpoints. Utilisez l'en-tête Authorization avec la valeur Bearer <Votre_Token> dans vos requêtes.

https://documenter.getpostman.com/view/29596074/2s9YR9aDAL

## Auteur
[Laseguue](https://github.com/Laseguue)
