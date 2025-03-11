from django.contrib import admin
from django.urls import path, include
from games.apps import GamesConfig
from games.views import HomeView, GamesDetailView, StatisticInteractionView

app_name = GamesConfig.name

urlpatterns = [
    #path('', HomeView.as_view(), name='home'),
    path("home/", HomeView.as_view(), name="home"),
    path("game_detail/<int:pk>/", GamesDetailView.as_view(), name="game_detail"),
    path("statistic/", StatisticInteractionView.as_view(), name="statistic"),

]
