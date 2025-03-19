# flake8: noqa
from django.urls import include, path
from django.views.decorators.cache import cache_page


from games.apps import GamesConfig
from games.views import (ChoiceView, CollaborativeFilteringView,
                         GameRecommendationsListView, GamesDetailView,
                         GamesListView, HomeView, InteractionCreateApiview,
                         InteractionRetrieveApiView, NearestNeighborsView,
                         PageRankView, StatisticInteractionView)

app_name = GamesConfig.name

# router = SimpleRouter()

urlpatterns = [
    path("games/", GamesListView.as_view(), name="game_list"),
    path("home/", HomeView.as_view(), name="home"),
    path(
        "games/<int:pk>/", cache_page(60)(GamesDetailView.as_view()), name="game_detail"
    ),
    path("statistic/", StatisticInteractionView.as_view(), name="statistic"),
    path("choice_user/", ChoiceView.as_view(), name="choice_user"),
    path(
        "recommendation/", GameRecommendationsListView.as_view(), name="recommendation"
    ),
    path("games_int/<int:pk>/", InteractionRetrieveApiView.as_view(), name="games_int"),
    path("prefer_add/", InteractionCreateApiview.as_view(), name="prefer_add"),
    path("page_rank/", PageRankView.as_view(), name="page-rank"),
    path("col_filter/", CollaborativeFilteringView.as_view(), name="col_filter"),
    path("near_neighbor/", NearestNeighborsView.as_view(), name="near_neighbor"),
]
