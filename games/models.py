from django.db import models

import users.models


class Games(models.Model):
    """Модель игры"""

    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Описание игры")
    release_date = models.DateField(auto_now_add=True)
    genre = models.ManyToManyField("Genre", related_name="games")
    developer = models.ForeignKey("Developer", on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    platforms = models.CharField(max_length=50, verbose_name="Игровая платформа")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return self.title


class Genre(models.Model):
    """Модель жанры игр"""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Developer(models.Model):
    """Модель разработчик и издатель игр"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, verbose_name="Описание и какие еще игры выпускали")

    class Meta:
        verbose_name = "Разработчик"
        verbose_name_plural = "Разработчики"

    def __str__(self):
        return self.name


class Interaction(models.Model):
    """Модель взаимодествия"""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания взаимодействия"
    )
    updated_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время последнего обновления взаимодействия"
    )
    playtime = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Время, проведенное в игре (в часах)",
    )
    is_favorite = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Пометка, является ли игра любимой",
    )

    class Meta:
        verbose_name = "Взаимодействие"
        verbose_name_plural = "Взаимодействия"

    def __str__(self):
        return f"{self.user}  {self.game} {self.rating}"
