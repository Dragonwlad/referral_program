# Generated by Django 3.2.16 on 2023-08-17 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20230817_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='my_invite_code',
            field=models.CharField(default='j8XjyQ', editable=False, max_length=6, unique=True, verbose_name='Инвайт-код для приглашения других пользователей'),
        ),
    ]