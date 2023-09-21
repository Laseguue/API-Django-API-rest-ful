from django.db import models
from .custom_user import CustomUser
from .project import Project

class Issue(models.Model):
    PRIORITIES = [('LOW', 'LOW'), ('MEDIUM', 'MEDIUM'), ('HIGH', 'HIGH')]
    TAGS = [('BUG', 'BUG'), ('FEATURE', 'FEATURE'), ('TASK', 'TASK')]
    STATUSES = [('TO DO', 'TO DO'), ('IN PROGRESS', 'IN PROGRESS'), ('FINISHED', 'FINISHED')]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices=STATUSES, max_length=15, default='TO DO')
    priority = models.CharField(choices=PRIORITIES, max_length=10)
    tag = models.CharField(choices=TAGS, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authored_issues')
    class Meta:
        ordering = ['created_time']