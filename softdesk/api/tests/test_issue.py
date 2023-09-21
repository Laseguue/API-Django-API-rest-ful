from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Issue, CustomUser, Project  

class TestIssue(APITestCase):
    url_issues = '/issues/'
    url_token_auth = '/token-auth/'
    url_projects = '/projects/'
    token = None
    
    def setUp(self):
        # Création de l'utilisateur
        user_data = {
            'username': 'issueuser',
            'password': 'issuepass123',
            'age': 30,
            'can_be_contacted': True,
            'can_data_be_shared': True
        }
        self.client.post('/users/', data=user_data)
        # Authentification de l'utilisateur
        data_auth = {
            'username': 'issueuser',
            'password': 'issuepass123'
        }
        response_auth = self.client.post(self.url_token_auth, data=data_auth)
        TestIssue.token = response_auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TestIssue.token)
        
        # Création d'un projet pour le test de Issue
        project_data = {
            'title': 'Project for Issue',
            'description': 'Description for Issue project',
            'type': 'BE'
        }
        response_project = self.client.post(self.url_projects, data=project_data)
        self.project_id = response_project.data['id']

    def test_issue_create_list(self):
        # Création de l'issue
        data = {
            'title': 'New Issue',
            'description': 'This is a new issue',
            'status': 'TO DO',
            'priority': 'HIGH',
            'tag': 'BUG',
            'project': self.project_id,
            'assigned_to': CustomUser.objects.get(username='issueuser').id
        }
        response_post = self.client.post(self.url_issues, data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        
        # Lister tous les issues
        response = self.client.get(self.url_issues)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_issue_retrieve_update_destroy(self):
        # Création initiale de l'issue
        data = {
            'title': 'Another Issue',
            'description': 'This is another issue',
            'status': 'TO DO',
            'priority': 'MEDIUM',
            'tag': 'FEATURE',
            'project': self.project_id,
            'assigned_to': CustomUser.objects.get(username='issueuser').id
        }
        response_post = self.client.post(self.url_issues, data=data)
        issue_id = response_post.data['id']
        
        # Récupérer
        response_get = self.client.get(f'/issues/{issue_id}/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        
        # Mettre à jour
        response_patch = self.client.patch(f'/issues/{issue_id}/', data={'title': 'Updated Issue'})
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        
        # Supprimer
        response_delete = self.client.delete(f'/issues/{issue_id}/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)