from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Games, Interaction
from games.serializers import InteractionSerializer
from games.services import get_games_from_cashe, collaborative_filtering, calculate_page_rank, k_nearest_neighbors


class GamesListView(ListView):
    model = Games
   # template_name = "games/game_list"

    # def get_queryset(self):
    #     return get_games_from_cashe()


class GamesDetailView(DetailView):
    model = Games



class HomeView(View):
    """Класс представление главной страницы веб-приложения."""
    model = Games
    template_name = "games/home.html"
    context_object_name = "home"



class StatisticInteractionView(LoginRequiredMixin, ListView):
    """Представление статистики рекомендаций для пользователя."""
    model = Interaction
    template_name = "games/statistic.html"
    context_object_name = "statistics"

    def get_queryset(self):
        return Interaction.objects.filter(user=self.request.user)



class InteractionCreateApiview(CreateAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

class InteractionRetrieveApiView(RetrieveAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

class PageRankView(APIView):
    def get(self, request):
        pr = calculate_page_rank()
        return Response(pr)

class CollaborativeFilteringView(APIView):
    def get(self, request):
        neighbors = collaborative_filtering()
        return Response(neighbors)

class NearestNeighborsView(APIView):
    def get(self, request):
        neighbors = k_nearest_neighbors()
        return Response(neighbors)

