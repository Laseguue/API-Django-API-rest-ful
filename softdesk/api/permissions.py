from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que l'auteur d'une ressource à la modifier.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsProjectContributor(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que les contributeurs d'un projet à y accéder.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.contributors.all()
