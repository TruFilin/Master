from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import GroupChat
User = get_user_model()
from .models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Храните пароль в зашифрованном виде
        user.save()
        return user
class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'members']