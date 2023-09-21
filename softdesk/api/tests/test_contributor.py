from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Contributor, CustomUser, Project  

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
        
        # Mettre à jour 
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