from rest_framework import generics, permissions
from .models import CustomUser, Project, Issue, Comment, Contributor
from .serializers import CustomUserSerializer, ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectContributor
from django.db import transaction
from rest_framework.permissions import AllowAny

# Vues pour User
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [permissions.IsAuthenticated()]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

# Vues pour Project
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

# Vues pour Contributor
class ContributorListCreateView(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

class ContributorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjectContributor]

    def destroy(self, request, *args, **kwargs):
        contributor = self.get_object()
        if not contributor.project.authors.filter(id=request.user.id).exists():
            return Response({"message": "Seul l'auteur du projet peut supprimer un contributeur."}, status=403)
        return super().destroy(request, *args, **kwargs)

# Vues pour Issue
class IssueListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def perform_create(self, serializer):
        contributor = Contributor.objects.get(user=self.request.user, project=serializer.validated_data['project'])
        issue = serializer.save(author=self.request.user)

class IssueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjectContributor]

# Vues pour Comment
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def perform_create(self, serializer):
        contributor = Contributor.objects.get(user=self.request.user, project=serializer.validated_data['issue'].project)
        comment = serializer.save(author=self.request.user)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjectContributor]
