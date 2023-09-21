from rest_framework import generics, permissions
from api.models import Comment, Contributor
from api.serializers import CommentSerializer
from api.permissions import IsAuthorOrReadOnly, IsProjectContributor

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