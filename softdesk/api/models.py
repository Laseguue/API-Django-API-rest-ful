from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    
    # Add these fields with custom related names
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_user_permissions",
        related_query_name="customuser",
    )

class Project(models.Model):
    TYPES = [('BE', 'back-end'), ('FE', 'front-end'), ('iOS', 'iOS'), ('Android', 'Android')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(choices=TYPES, max_length=10)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')

class Contributor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')

class Issue(models.Model):
    PRIORITIES = [('Low', 'LOW'), ('Medium', 'MEDIUM'), ('High', 'HIGH')]
    TAGS = [('Bug', 'BUG'), ('Feature', 'FEATURE'), ('Task', 'TASK')]
    STATUSES = [('To Do', 'TO DO'), ('In Progress', 'IN PROGRESS'), ('Finished', 'FINISHED')]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices=STATUSES, max_length=15, default='To Do')
    priority = models.CharField(choices=PRIORITIES, max_length=10)
    tag = models.CharField(choices=TAGS, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_issues')

class Comment(models.Model):
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(unique=True, auto_created=True, primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
