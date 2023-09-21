from rest_framework import generics, permissions
from api.models import Issue, Contributor
from api.serializers import IssueSerializer
from api.permissions import IsAuthorOrReadOnly, IsProjectContributor

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
