from rest_framework import generics, permissions
from api.models import CustomUser
from api.serializers import CustomUserSerializer
from api.permissions import IsAuthorOrReadOnly
from rest_framework.permissions import AllowAny

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