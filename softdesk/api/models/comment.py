from django.db import models
from .issue import Issue
from .custom_user import CustomUser
import uuid  

class Comment(models.Model):
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(unique=True, auto_created=True, primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authored_comments')
    class Meta:
        ordering = ['created_time']