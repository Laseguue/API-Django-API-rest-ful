from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Project, Contributor, Issue, Comment

class TestCustomUser(APITestCase):
    url_users = '/users/'
    url_token_auth = '/token-auth/'
    token = None

    def setUp(self):
        # Création de l'utilisateur
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'age': 25,
            'can_be_contacted': True,
            'can_data_be_shared': False
        }
        self.client.post(self.url_users, data=data)
        # Authentification de l'utilisateur
        data_auth = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        response_auth = self.client.post(self.url_token_auth, data=data_auth)
        TestCustomUser.token = response_auth.data['access']

    def test_user_create(self):
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_user_authentication(self):
        self.assertIsNotNone(TestCustomUser.token)

    def test_user_list(self):
        # Utilisation du token pour l'authentification
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TestCustomUser.token)
        
        response = self.client.get(self.url_users)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_retrieve_update_destroy(self):
        user_id = CustomUser.objects.get(username='newuser').id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TestCustomUser.token)
        
        # Récupérer
        response_get = self.client.get(f'/users/{user_id}/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        
        # Mettre à jour
        response_patch = self.client.patch(f'/users/{user_id}/', data={'age': 21})
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        
        # Supprimer
        response_delete = self.client.delete(f'/users/{user_id}/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

class TestProject(APITestCase):
    url_projects = '/projects/'
    url_token_auth = '/token-auth/'
    token = None
    
    def setUp(self):
        # Création de l'utilisateur
        data = {
            'username': 'projectuser',
            'password': 'projectpass123',
            'age': 30,
            'can_be_contacted': True,
            'can_data_be_shared': True
        }
        self.client.post('/users/', data=data)
        # Authentification de l'utilisateur
        data_auth = {
            'username': 'projectuser',
            'password': 'projectpass123'
        }
        response_auth = self.client.post(self.url_token_auth, data=data_auth)
        TestProject.token = response_auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TestProject.token)

    def test_project_create_list(self):
        # Création du projet
        data = {
            'title': 'New Project',
            'description': 'This is a new project',
            'type': 'BE'
        }
        response_post = self.client.post(self.url_projects, data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        
        # Lister tous les projets
        response = self.client.get(self.url_projects)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_retrieve_update_destroy(self):
        # Création initiale du projet
        data = {
            'title': 'Another Project',
            'description': 'This is another project',
            'type': 'BE'
        }
        response_post = self.client.post(self.url_projects, data=data)
        project_id = response_post.data['id']
        
        # Récupérer
        response_get = self.client.get(f'/projects/{project_id}/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        
        # Mettre à jour
        response_patch = self.client.patch(f'/projects/{project_id}/', data={'title': 'Updated Project'})
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        
        # Supprimer
        response_delete = self.client.delete(f'/projects/{project_id}/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

class TestContributor(APITestCase):
    url_contributors = '/contributors/'
    url_token_auth = '/token-auth/'
    url_projects = '/projects/'
    token = None
    
    def setUp(self):
        # Création de l'utilisateur
        user_data = {
            'username': 'contributoruser',
            'password': 'contributorpass123',
            'age': 30,
            'can_be_contacted': True,
            'can_data_be_shared': True
        }
        self.client.post('/users/', data=user_data)
        # Authentification de l'utilisateur
        data_auth = {
            'username': 'contributoruser',
            'password': 'contributorpass123'
        }
        response_auth = self.client.post(self.url_token_auth, data=data_auth)
        TestContributor.token = response_auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TestContributor.token)
        
        # Création d'un projet pour le test de Contributor
        project_data = {
            'title': 'Project for Contributor',
            'description': 'Description for Contributor project',
            'type': 'BE'
        }
        response_project = self.client.post(self.url_projects, data=project_data)
        self.project_id = response_project.data['id']

    def test_contributor_create_list(self):
        # Création du contributeur
        user = CustomUser.objects.get(username='contributoruser')
        data = {
            'user': user.id,
            'project': self.project_id
        }
        response_post = self.client.post(self.url_contributors, data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        
        # Lister tous les contributeurs
        response = self.client.get(self.url_contributors)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contributor_retrieve_update_destroy(self):
        # Création initiale du contributeur
        user = CustomUser.objects.get(username='contributoruser')
        data = {
            'user': user.id,
            'project': self.project_id
        }
        response_post = self.client.post(self.url_contributors, data=data)
        contributor_id = response_post.data['id']
        
        # Récupérer
        response_get = self.client.get(f'/contributors/{contributor_id}/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        
        # Mettre à jour (dans ce cas, c'est un peu artificiel car un contributeur n'a que deux champs, et ils sont tous deux clés étrangères, mais je vais faire une mise à jour du champ `user` pour l'exemple)
        new_user_data = {
            'username': 'updatedcontributoruser',
            'password': 'updatedcontributorpass123',
            'age': 32,
            'can_be_contacted': True,
            'can_data_be_shared': True
        }
        response_new_user = self.client.post('/users/', data=new_user_data)
        updated_user_id = response_new_user.data['id']
        
        response_patch = self.client.patch(f'/contributors/{contributor_id}/', data={'user': updated_user_id})
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        
        # Supprimer
        response_delete = self.client.delete(f'/contributors/{contributor_id}/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

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
