from django.db import models
from .custom_user import CustomUser

class Project(models.Model):
    TYPES = [('BE', 'BE'), ('FE', 'FE'), ('iOS', 'iOS'), ('Android', 'Android')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(choices=TYPES, max_length=10)
    created_time = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(CustomUser, related_name='authored_projects')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects')
    class Meta:
        ordering = ['created_time']