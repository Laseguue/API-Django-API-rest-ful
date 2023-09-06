from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser, Project, Contributor, Issue, Comment

class CustomUserTests(APITestCase):

    def setUp(self):
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

class ProjectTests(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='testpass123', age=20)
        self.user2 = CustomUser.objects.create_user(username='user2', password='testpass123', age=25)
        self.project = Project.objects.create(title="Test Project", description="Description", type="BE", author=self.user1)
        self.client.force_authenticate(user=self.user1)

    def test_create_project(self):
        data = {
            'title': 'New Project',
            'description': 'Project Description',
            'type': 'BE'
        }
        response = self.client.post(reverse('project-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_update_project_by_author(self):
        data = {
            'description': 'Updated Description'
        }
        response = self.client.patch(reverse('project-retrieve-update-destroy', args=[self.project.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, 'Updated Description')

    def test_prevent_update_project_by_other(self):
        self.client.force_authenticate(user=self.user2)
        data = {
            'description': 'Another Update'
        }
        response = self.client.patch(reverse('project-retrieve-update-destroy', args=[self.project.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_projects(self):
        response = self.client.get(reverse('project-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_project_by_author(self):
        response = self.client.delete(reverse('project-retrieve-update-destroy', args=[self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

class ContributorTests(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='testpass123', age=20)
        self.user2 = CustomUser.objects.create_user(username='user2', password='testpass123', age=25)
        self.project = Project.objects.create(title="Test Project", description="Description", type="BE", author=self.user1)
        self.contributor = Contributor.objects.create(user=self.user2, project=self.project)
        self.client.force_authenticate(user=self.user1)

    def test_add_contributor_to_project(self):
        data = {
            'user': self.user2.id,
            'project': self.project.id
        }
        response = self.client.post(reverse('contributor-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contributor.objects.count(), 2)

    def test_remove_contributor_from_project(self):
        response = self.client.delete(reverse('contributor-retrieve-update-destroy', args=[self.contributor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contributor.objects.count(), 0)

class IssueTests(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='testpass123', age=20)
        self.user2 = CustomUser.objects.create_user(username='user2', password='testpass123', age=25)
        self.project = Project.objects.create(title="Test Project", description="Description", type="BE", author=self.user1)
        self.issue = Issue.objects.create(title="Test Issue", description="Issue Description", priority="Low", tag="Bug", project=self.project, assigned_to=self.user2, author=self.user1)
        self.client.force_authenticate(user=self.user1)

    def test_create_issue(self):
        data = {
            'title': 'New Issue',
            'description': 'Issue Description',
            'priority': 'Low',
            'tag': 'Bug',
            'project': self.project.id,
            'assigned_to': self.user2.id
        }
        response = self.client.post(reverse('issue-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 2)

    def test_update_issue_by_author(self):
        data = {
            'description': 'Updated Issue Description'
        }
        response = self.client.patch(reverse('issue-retrieve-update-destroy', args=[self.issue.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertEqual(self.issue.description, 'Updated Issue Description')

    def test_prevent_update_issue_by_other(self):
        self.client.force_authenticate(user=self.user2)
        data = {
            'description': 'Another Update'
        }
        response = self.client.patch(reverse('issue-retrieve-update-destroy', args=[self.issue.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_issues(self):
        response = self.client.get(reverse('issue-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_issue_by_author(self):
        response = self.client.delete(reverse('issue-retrieve-update-destroy', args=[self.issue.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Issue.objects.count(), 0)

class CommentTests(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='testpass123', age=20)
        self.project = Project.objects.create(title="Test Project", description="Description", type="BE", author=self.user1)
        self.issue = Issue.objects.create(title="Test Issue", description="Issue Description", priority="Low", tag="Bug", project=self.project, assigned_to=self.user1, author=self.user1)
        self.comment = Comment.objects.create(description="Test Comment", issue=self.issue, author=self.user1)
        self.client.force_authenticate(user=self.user1)

    def test_create_comment(self):
        data = {
            'description': 'New Comment',
            'issue': self.issue.id
        }
        response = self.client.post(reverse('comment-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_update_comment_by_author(self):
        data = {
            'description': 'Updated Comment'
        }
        response = self.client.patch(reverse('comment-retrieve-update-destroy', args=[str(self.comment.uuid)]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.description, 'Updated Comment')

    def test_prevent_update_comment_by_other(self):
        user2 = CustomUser.objects.create_user(username='user2', password='testpass123', age=25)
        self.client.force_authenticate(user=user2)
        data = {
            'description': 'Another Comment Update'
        }
        response = self.client.patch(reverse('comment-retrieve-update-destroy', args=[str(self.comment.uuid)]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_comments(self):
        response = self.client.get(reverse('comment-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_comment_by_author(self):
        response = self.client.delete(reverse('comment-retrieve-update-destroy', args=[str(self.comment.uuid)]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user', password='testpass123', age=20)
        self.token_url = reverse('token_obtain_pair')

    def test_get_jwt_token(self):
        data = {
            'username': 'user',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_jwt_token(self):
        data = {
            'username': 'user',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data)
        refresh_token = response.data['refresh']
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)