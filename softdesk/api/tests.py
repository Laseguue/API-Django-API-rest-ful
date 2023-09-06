from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser

class CustomUserTests(APITestCase):

    def setUp(self):
        # Création de deux utilisateurs pour les tests
        self.user1 = CustomUser.objects.create_user(username='user1', password='testpass123', age=20)
        self.user2 = CustomUser.objects.create_user(username='user2', password='testpass123', age=25)
        self.token_url = reverse('token_obtain_pair')

    def test_create_user(self):
        data = {
            'username': 'user3',
            'password': 'testpass123',
            'age': 18
        }
        response = self.client.post(reverse('user-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_update_user_by_author(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'age': 21
        }
        response = self.client.patch(reverse('user-retrieve-update-destroy', args=[self.user1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.age, 21)

    def test_prevent_update_user_by_other(self):
        self.client.force_authenticate(user=self.user2)
        data = {
            'age': 21
        }
        response = self.client.patch(reverse('user-retrieve-update-destroy', args=[self.user1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users(self):
        response = self.client.get(reverse('user-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_user_by_author(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('user-retrieve-update-destroy', args=[self.user1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_get_token(self):
        data = {
            'username': 'user1',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
