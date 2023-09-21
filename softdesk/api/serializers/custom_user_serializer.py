from rest_framework import serializers
from api.models import CustomUser

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