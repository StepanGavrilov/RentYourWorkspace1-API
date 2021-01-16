from django.db import models

from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    """
    Аккаунт пользователя
    """

    username = models.CharField(
        db_index=True,
        unique=True,
        max_length=32,
        blank=False,
        verbose_name='Username'
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=32,
        blank=False,
        verbose_name='E-mail'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Staff'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Superuser'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return f'Username: {self.username} Id: {self.id}'
