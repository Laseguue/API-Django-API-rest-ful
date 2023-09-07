from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import CustomUser, Project, Contributor, Issue, Comment

class SoftDeskTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "password": "testpass123",
            "age": 20,
            "can_be_contacted": True,
            "can_data_be_shared": True
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.client.force_authenticate(self.user)  # Authentifier l'utilisateur pour les requêtes

    def test_user_registration_and_authentication(self):
        # Test d'enregistrement d'un nouvel utilisateur
        response = self.client.post("/users/", self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("username", response.data)

        # Test de l'authentification
        response = self.client.post("/token-auth/", {"username": "testuser", "password": "testpass123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

        # Test de l'échec de l'authentification avec un mauvais mot de passe
        response = self.client.post("/token-auth/", {"username": "testuser", "password": "wrongpass"})
        self.assertEqual(response.status_code, 401)

    def test_project_crud_operations(self):
        project_data = {"title": "Test Project", "description": "This is a test project", "type": "BE"}
        
        # Test de création de projet
        response = self.client.post("/projects/", project_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("title", response.data)

        project_id = response.data["id"]

        # Test de mise à jour du projet
        updated_data = {"title": "Updated Project", "description": "Updated description", "type": "FE"}
        response = self.client.put(f"/projects/{project_id}/", updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Updated Project")

        # Test de suppression du projet
        response = self.client.delete(f"/projects/{project_id}/")
        self.assertEqual(response.status_code, 204)

    def test_issue_crud_operations(self):
        project = Project.objects.create(title="Test Project", description="This is a test project", type="BE")
        issue_data = {
            "title": "Test Issue", 
            "description": "This is a test issue",
            "status": "TO DO",
            "priority": "MEDIUM",
            "tag": "BUG",
            "project": project.id,
            "assigned_to": self.user.id,
        }
        # Test de création d'issue
        response = self.client.post("/issues/", issue_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("title", response.data)

        issue_id = response.data["id"]

        # Test de mise à jour d'issue
        updated_data = {
            "title": "Updated Issue", 
            "description": "Updated description",
            "status": "IN PROGRESS",
            "priority": "HIGH",
            "tag": "TASK",
        }
        response = self.client.put(f"/issues/{issue_id}/", updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Updated Issue")

        # Test de suppression d'issue
        response = self.client.delete(f"/issues/{issue_id}/")
        self.assertEqual(response.status_code, 204)

    def test_comments_on_issues(self):
        project = Project.objects.create(title="Test Project", description="This is a test project", type="BE")
        issue = Issue.objects.create(
            title="Test Issue", 
            description="This is a test issue",
            status="TO DO",
            priority="MEDIUM",
            tag="BUG",
            project=project,
            assigned_to=self.user
        )
        comment_data = {
            "description": "This is a test comment",
            "issue": issue.id,
        }

        # Test de création de commentaire
        response = self.client.post("/comments/", comment_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("description", response.data)

        comment_id = response.data["uuid"]

        # Test de mise à jour de commentaire
        updated_data = {"description": "Updated comment"}
        response = self.client.put(f"/comments/{comment_id}/", updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Updated comment")

        # Test de suppression de commentaire
        response = self.client.delete(f"/comments/{comment_id}/")
        self.assertEqual(response.status_code, 204)

    def test_failure_scenarios(self):

        # Test de création d'un utilisateur avec un âge inférieur à 15 ans
        underage_data = {
            "username": "underageuser",
            "password": "testpass123",
            "age": 14,
            "can_be_contacted": True,
            "can_data_be_shared": True
        }
        response = self.client.post("/users/", underage_data)
        self.assertEqual(response.status_code, 400)

        # Test de création d'un projet sans titre
        project_data = {"description": "This is a test project", "type": "BE"}
        response = self.client.post("/projects/", project_data)
        self.assertEqual(response.status_code, 400)

        # Test de création d'un issue sans titre
        issue_data = {
            "description": "This is a test issue",
            "status": "TO DO",
            "priority": "MEDIUM",
            "tag": "BUG",
            "project": 1,
            "assigned_to": self.user.id,
        }
        response = self.client.post("/issues/", issue_data)
        self.assertEqual(response.status_code, 400)

        # Test de création d'un commentaire sans description
        comment_data = {"issue": 1}
        response = self.client.post("/comments/", comment_data)
        self.assertEqual(response.status_code, 400)

        # Test de création d'un projet avec un type non valide
        project_data_invalid_type = {"title": "Test Project", "description": "This is a test project", "type": "INVALID"}
        response = self.client.post("/projects/", project_data_invalid_type)
        self.assertEqual(response.status_code, 400)

        # Test d'accès à un projet par un non-contributeur
        non_contributor = CustomUser.objects.create_user(username="noncontributor", password="testpass123", age=20)
        self.client.force_authenticate(non_contributor)
        response = self.client.get("/projects/1/")
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test d'accès à un issue par un non-contributeur du projet associé
        response = self.client.get("/issues/1/")
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test d'accès à un commentaire par un non-contributeur de l'issue associée
        response = self.client.get("/comments/1/")
        self.assertEqual(response.status_code, 403)  # Forbidden
