# flake8: noqa
from django.contrib.auth.models import AbstractUser
from django.db import models
from games.models import Games, Genre


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажи почту"
    )

    preferred_genres = models.ManyToManyField(
        "games.Genre", verbose_name="Любимые жанры", blank=True
    )

    preferred_platforms = models.ManyToManyField(
        "games.Games",
        through="UserPlatform",
        related_name="preferred_by",
        verbose_name="Любимые платформы",
        blank=True,
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class UserPlatform(models.Model):
    """Промежуточная модель для связи с платформами"""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    game = models.ForeignKey("games.Games", on_delete=models.CASCADE)
    platform = models.CharField(
        max_length=50,
        verbose_name="Игровая платформа",
        choices=[
        ],
    )

    class Meta:

        verbose_name = "User_platform"
        verbose_name_plural = "Users_platforms"

    def __str__(self):
        return self.user
