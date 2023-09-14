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
