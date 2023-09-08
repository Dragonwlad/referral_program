from django.db import models
from secrets import token_urlsafe
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    """Модель данных для пользователей."""
    username = None
    email = None
    phone_number = PhoneNumberField(
        'Номер телефона',
        # region='RU', если требуются номера только из РФ
        max_length=12,
        unique=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=4,
        blank=True)
    my_invite_code = models.CharField(
        'Инвайт-код для приглашения других пользователей',
        default=token_urlsafe(4),
        max_length=6,
        unique=True,
        editable=False)
    inviter_code = models.CharField(
        'Инвайт-код пригласившего',
        max_length=6,
        blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.phone_number)
