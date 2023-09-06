from rest_framework import serializers
from .models import CustomUser, Project, Contributor, Issue, Comment

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared')
    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("Vous devez avoir plus de 15 ans pour vous inscrire.")
        return value

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'created_time', 'author')

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'project')

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'status', 'priority', 'tag', 'project', 'assigned_to', 'created_time', 'author')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('uuid', 'description', 'issue', 'created_time', 'author')
