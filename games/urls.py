from django.contrib import admin
from django.urls import path, include
from games.apps import GamesConfig
from games.views import HomeView

app_name = GamesConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
]
