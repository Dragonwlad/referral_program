# Generated by Django 3.2.16 on 2023-08-17 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_my_invite_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.AlterField(
            model_name='user',
            name='my_invite_code',
            field=models.CharField(default='L8FL5Q', editable=False, max_length=6, unique=True, verbose_name='Мой инвайт-код для приглашения других пользователей'),
        ),
    ]
