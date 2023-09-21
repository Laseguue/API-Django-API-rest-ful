from rest_framework import serializers
from api.models import Project
from .contributor_serializer import ContributorSerializer

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