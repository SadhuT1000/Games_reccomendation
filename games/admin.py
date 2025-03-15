from django.contrib import admin

from games.models import Games, Genre, Developer, Interaction


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'rating',
        'platforms',
        'price',

    )
    search_fields = (
        'title',
    )



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'game',
        'rating',
        'game_count',
        'genre_count',
        'playtime',


    )
    search_fields = (
        'game',
    )

