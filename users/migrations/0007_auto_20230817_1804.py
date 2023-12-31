# Generated by Django 3.2.16 on 2023-08-17 15:04

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_my_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=4, verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='my_invite_code',
            field=models.CharField(default='NgNs0Q', editable=False, max_length=6, unique=True, verbose_name='Инвайт-код для приглашения других пользователей'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=11, region='RU', unique=True, verbose_name='Номер телефона'),
        ),
    ]
