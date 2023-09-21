from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Comment, CustomUser, Project, Issue  

class TestComment(APITestCase):
    url_comments = '/comments/'
    url_token_auth = '/token-auth/'
    url_projects = '/projects/'
    url_issues = '/issues/'
    token = None
    
    def setUp(self):
        # Création de l'utilisateur
        user_data = {
            'username': 'commentuser',
            'password': 'commentpass123',
            'age': 30,
            'can_be_contacted': True,
            'can_data_be_shared': True
        }
        self.client.post('/users/', data=user_data)
        # Authentification de l'utilisateur
        data_auth = {
            'username': 'commentuser',
            'password': 'commentpass123'
        }
        response_auth = self.client.post(self.url_token_auth, data=data_auth)
        TestComment.token = response_auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TestComment.token)
        
        # Création d'un projet pour le test de Comment
        project_data = {
            'title': 'Project for Comment',
            'description': 'Description for Comment project',
            'type': 'FE'
        }
        response_project = self.client.post(self.url_projects, data=project_data)
        self.project_id = response_project.data['id']

        # Création d'une issue pour le test de Comment
        issue_data = {
            'title': 'Issue for Comment',
            'description': 'Description for Comment issue',
            'status': 'TO DO',
            'priority': 'LOW',
            'tag': 'TASK',
            'project': self.project_id,
            'assigned_to': CustomUser.objects.get(username='commentuser').id
        }
        response_issue = self.client.post(self.url_issues, data=issue_data)
        self.issue_id = response_issue.data['id']

    def test_comment_create_list(self):
        # Création du commentaire
        data = {
            'description': 'This is a new comment',
            'issue': self.issue_id
        }
        response_post = self.client.post(self.url_comments, data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        
        # Lister tous les commentaires
        response = self.client.get(self.url_comments)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_retrieve_update_destroy(self):
        # Création initiale du commentaire
        data = {
            'description': 'Another comment',
            'issue': self.issue_id
        }
        response_post = self.client.post(self.url_comments, data=data)
        comment_uuid = response_post.data['uuid']
        
        # Récupérer
        response_get = self.client.get(f'/comments/{comment_uuid}/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        
        # Mettre à jour
        response_patch = self.client.patch(f'/comments/{comment_uuid}/', data={'description': 'Updated Comment'})
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        
        # Supprimer
        response_delete = self.client.delete(f'/comments/{comment_uuid}/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)