from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязательное поле!')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(

                                password=password,
                                phone_number=phone_number)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
