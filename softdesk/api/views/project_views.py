from rest_framework import generics, permissions
from django.db import transaction
from api.models import Project, Contributor
from api.serializers import ProjectListSerializer, ProjectDetailSerializer
from api.permissions import IsAuthorOrReadOnly, IsProjectContributor

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        project.authors.add(self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjectContributor]
