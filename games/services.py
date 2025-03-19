# flake8: noqa
import networkx as nx
from django.core.cache import cache
from sklearn.neighbors import NearestNeighbors

from config.settings import CACHE_ENABLED
from games.models import Games, Interaction
from users.models import User
from django.db.models import Avg


def get_games_from_cashe():
    """Получает по играм из кэша, если нет то из бд"""
    if not CACHE_ENABLED:
        return Games.objects.all()
    key = "games_list"
    games = cache.get(key)
    if games is not None:
        return games
    cache.set(key, games)
    return games


def calculate_page_rank():

    G = nx.DiGraph()


    for game in Games.objects.all():
        G.add_node(game.id)


    for interaction in Interaction.objects.all():
        G.add_edge(interaction.game.id, interaction.user.id)


    pr = nx.pagerank(G)

    return pr


def collaborative_filtering():

    data = []
    for user in User.objects.all():
        user_ratings = []
        for game in Games.objects.all():
            try:
                rating = Interaction.objects.get(user=user, game=game).rating
            except Interaction.DoesNotExist:
                rating = 0
            user_ratings.append(rating)
        data.append(user_ratings)


    model = NearestNeighbors(metric="cosine")
    model.fit(data)


    neighbors = model.kneighbors(data, n_neighbors=1)

    return neighbors


def k_nearest_neighbors():

    data = []
    for user in User.objects.all():
        user_features = []

        user_features.append(
            Interaction.objects.filter(user=user).aggregate(Avg("rating"))[
                "rating__avg"
            ]
        )
        data.append(user_features)


    model = NearestNeighbors(metric="euclidean")
    model.fit(data)


    neighbors = model.kneighbors(data, n_neighbors=1)

    return neighbors
