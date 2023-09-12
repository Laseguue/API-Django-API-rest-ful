from rest_framework import serializers
from .models import CustomUser, Project, Issue, Comment, Contributor

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'age', 'can_be_contacted', 'can_data_be_shared')
    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("Vous devez avoir plus de 15 ans pour vous inscrire.")
        return value
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'created_time')

class ProjectDetailSerializer(ProjectListSerializer):
    contributors = serializers.SerializerMethodField()

    class Meta(ProjectListSerializer.Meta):
        fields = ProjectListSerializer.Meta.fields + ('contributors',)

    def get_contributors(self, obj):
        return ContributorSerializer(obj.contributor_set.all(), many=True).data

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'project')

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'status', 'priority', 'tag', 'project', 'assigned_to', 'created_time')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('uuid', 'description', 'issue', 'created_time')
