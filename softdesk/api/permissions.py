from rest_framework import permissions
from .models import Contributor, Project, Comment, CustomUser

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que l'auteur d'une ressource à la modifier.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif isinstance(obj, CustomUser):
            return obj == request.user
        elif isinstance(obj, Contributor):
            return obj.project.author == request.user
        return obj.author == request.user

class IsProjectContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.author == request.user or Contributor.objects.filter(user=request.user, project=obj).exists()
        elif isinstance(obj, Comment):
            project = obj.issue.project
            return Contributor.objects.filter(user=request.user, project=project).exists()
        elif hasattr(obj, 'project'):
            return Contributor.objects.filter(user=request.user, project=obj.project).exists()
        return False

