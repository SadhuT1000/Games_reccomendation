from django.contrib.auth.models import AbstractUser
from django.db import models
from games.models import Games, Genre
import games.models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Укажи почту"
    )


    preferred_genres = models.ManyToManyField('games.Genre',
        verbose_name="Любимые жанры",
        blank=True
    )


    preferred_platforms = models.ManyToManyField('games.Games',
        through='UserPlatform',  # Создаем промежуточную модель
        related_name='preferred_by',
        verbose_name="Любимые платформы",
        blank=True
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
        verbose_name="Твой аватар",
        help_text="Загрузи фото",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email



class UserPlatform(models.Model):
    """Промежуточная модель для связи с платформами"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    game = models.ForeignKey('games.Games', on_delete=models.CASCADE)
    platform = models.CharField(
        max_length=50,
        verbose_name="Игровая платформа",
        choices=[(p, p) for p in Games.objects.values_list('platforms', flat=True).distinct()]
    )

    class Meta:

        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.user


# class User(AbstractUser):
#     """Модель поьзователя"""
#
#     username = None
#
#     email = models.EmailField(
#         unique=True, verbose_name="Почта", help_text="Укажи почту"
#     )
#
#     preferred_genres = models.ManyToManyField(
#         games.models.Genre, verbose_name="Preferred Genres", blank=True
#     )
#
#     phone = models.CharField(
#         max_length=35,
#         blank=True,
#         null=True,
#         verbose_name="Телефон",
#         help_text="Телефон напиши",
#     )
#
#     avatar = models.ImageField(
#         upload_to="users/avatars",
#         blank=True,
#         null=True,
#         verbose_name="твой аватар",
#         help_text="Грузи фото",
#     )
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         verbose_name = "User"
#         verbose_name_plural = "Users"
#
#     def __str__(self):
#         return self.email
