"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (
    UserListCreateView, UserRetrieveUpdateDestroyView,
    ProjectListCreateView, ProjectRetrieveUpdateDestroyView,
    ContributorListCreateView, ContributorRetrieveUpdateDestroyView,
    IssueListCreateView, IssueRetrieveUpdateDestroyView,
    CommentListCreateView, CommentRetrieveUpdateDestroyView
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    # URLs pour Project
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project-retrieve-update-destroy'),

    # URLs pour Contributor
    path('contributors/', ContributorListCreateView.as_view(), name='contributor-list-create'),
    path('contributors/<int:pk>/', ContributorRetrieveUpdateDestroyView.as_view(), name='contributor-retrieve-update-destroy'),

    # URLs pour Issue
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('issues/<int:pk>/', IssueRetrieveUpdateDestroyView.as_view(), name='issue-retrieve-update-destroy'),

    # URLs pour Comment
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),

    path('token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]