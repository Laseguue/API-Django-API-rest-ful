from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (UserListCreateView, UserRetrieveUpdateDestroyView,
                      ProjectListCreateView, ProjectRetrieveUpdateDestroyView,
                      ContributorListCreateView, ContributorRetrieveUpdateDestroyView,
                      IssueListCreateView, IssueRetrieveUpdateDestroyView,
                      CommentListCreateView, CommentRetrieveUpdateDestroyView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project-retrieve-update-destroy'),
    path('contributors/', ContributorListCreateView.as_view(), name='contributor-list-create'),
    path('contributors/<int:pk>/', ContributorRetrieveUpdateDestroyView.as_view(), name='contributor-retrieve-update-destroy'),
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('issues/<int:pk>/', IssueRetrieveUpdateDestroyView.as_view(), name='issue-retrieve-update-destroy'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<uuid:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),
]
