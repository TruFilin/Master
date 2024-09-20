# Generated by Django 5.1.1 on 2024-09-18 14:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_groupchat_members_groupchatmembership'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupchat',
            name='members',
            field=models.ManyToManyField(related_name='group_chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
