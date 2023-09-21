from rest_framework import serializers
from api.models import Issue

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'status', 'priority', 'tag', 'project', 'assigned_to', 'created_time')