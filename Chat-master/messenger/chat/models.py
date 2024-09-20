from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='группы',
        blank=True,
        related_name='customuser_set',
        help_text='Группы, к которым принадлежит этот пользователь.',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='права пользователя',
        blank=True,
        related_name='customuser_set_permissions',
        help_text='Конкретные права для этого пользователя.',
        related_query_name='customuser_permission',
    )

    # Добавьте поле для аватара
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png')  # Путь для загрузки аватара


class GroupChat(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='group_chats')  # Убедитесь, что это поле присутствует

    def __str__(self):
        return self.name


class GroupChatMembership(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Message(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"