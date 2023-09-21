from rest_framework import generics, permissions
from api.models import Contributor
from api.serializers import ContributorSerializer
from api.permissions import IsAuthorOrReadOnly, IsProjectContributor

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