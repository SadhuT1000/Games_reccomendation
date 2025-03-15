from config.settings import CACHE_ENABLED
from games.models import Games, Interaction
from django.core.cache import cache
import networkx as nx
from sklearn.neighbors import NearestNeighbors

from users.models import User


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
    # Создание графа
    G = nx.DiGraph()

    # Добавление узлов (игр)
    for game in Games.objects.all():
        G.add_node(game.id)

    # Добавление рёбер (взаимодействий)
    for interaction in Interaction.objects.all():
        G.add_edge(interaction.game.id, interaction.user.id)

    # Вычисление PageRank
    pr = nx.pagerank(G)

    return pr



def collaborative_filtering():
    # Сбор данных о предпочтениях пользователей
    data = []
    for user in User.objects.all():
        user_ratings = []
        for game in Game.objects.all():
            try:
                rating = Interaction.objects.get(user=user, game=game).rating
            except Interaction.DoesNotExist:
                rating = 0
            user_ratings.append(rating)
        data.append(user_ratings)

    # Создание модели
    model = NearestNeighbors(metric='cosine')
    model.fit(data)

    # Нахождение ближайших соседей для каждого пользователя
    neighbors = model.kneighbors(data, n_neighbors=5)

    return neighbors


def k_nearest_neighbors():
    # Сбор данных о пользователях
    data = []
    for user in User.objects.all():
        user_features = []
        # Добавление признаков пользователя (например, средние оценки игр)
        user_features.append(Interaction.objects.filter(user=user).aggregate(Avg('rating'))['rating__avg'])
        data.append(user_features)

    # Создание модели
    model = NearestNeighbors(metric='euclidean')
    model.fit(data)

    # Нахождение ближайших соседей для каждого пользователя
    neighbors = model.kneighbors(data, n_neighbors=5)

    return neighbors