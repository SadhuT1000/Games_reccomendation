from django.contrib.auth.models import AbstractUser
from django.db import models

import games.models


class User(AbstractUser):
    """Модель поьзователя"""

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажи почту"
    )

    preferred_genres = models.ManyToManyField(
        games.models.Genre, verbose_name="Preferred Genres", blank=True
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Телефон напиши",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="твой аватар",
        help_text="Грузи фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
