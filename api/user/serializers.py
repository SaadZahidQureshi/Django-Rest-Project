from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.core.choices import Roles


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']


class UpdateUserRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=Roles.choices)


class UpdateUserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
