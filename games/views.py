# flake8: noqa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Games, Genre, Interaction
from games.serializers import InteractionSerializer
from games.services import (calculate_page_rank, collaborative_filtering,
                            k_nearest_neighbors)


class GamesListView(ListView):
    model = Games
    template_name = "games/game_list"


class GamesDetailView(DetailView):
    model = Games


class HomeView(TemplateView):
    """Класс представление главной страницы веб-приложения."""

    model = Games
    template_name = "games/home.html"
    # context_object_name = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['games'] = Games.objects.all()
        return context


class StatisticInteractionView(LoginRequiredMixin, ListView):
    """Представление статистики рекомендаций для пользователя."""

    model = Interaction
    template_name = "games/statistic.html"
    context_object_name = "statistics"

    def get_queryset(self):
        return Interaction.objects.filter(user=self.request.user)


class ChoiceView(LoginRequiredMixin, ListView):
    model = Interaction
    template_name = "games/choice_user.html"
    context_object_name = "interactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        popular_games = (
            Interaction.objects.values("game")
            .annotate(count=Count("game"))
            .order_by("-count")[:10]
        )
        favorite_games = (
            Interaction.objects.filter(is_favorite=True)
            .values("game")
            .annotate(count=Count("game"))
            .order_by("-count")[:10]
        )
        rated_games = (
            Interaction.objects.filter(rating__isnull=False)
            .values("game__title")
            .annotate(average_rating=Avg("rating"))
            .order_by("-average_rating")[:10]
        )
        context["popular_games"] = popular_games
        context["favorite_games"] = favorite_games
        context["rated_games"] = rated_games

        # Предпочтения
        context["genres"] = Genre.objects.all()
        context["platforms"] = Games.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        try:

            selected_genres = request.POST.getlist("genres")
            selected_platforms = request.POST.getlist("platforms")

            user = request.user

            user.preferred_genres.set(selected_genres)
            user.preferred_platforms.set(selected_platforms)
            user.save()

            return redirect("choice")
        except Exception as e:
            return HttpResponseBadRequest(
                f"Ошибка при сохранении предпочтений: {str(e)}"
            )


class GameRecommendationsListView(ListView):
    model = Games
    template_name = "recommendations.html"
    context_object_name = "games"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recommended_games = Games.objects.annotate(
            avg_rating=Avg("interaction__rating"),
            interaction_count=Count("interaction"),
        ).order_by("-interaction_count", "-avg_rating")[:10]

        top_games = Games.objects.annotate(
            avg_rating=Avg("interaction__rating")
        ).order_by("-avg_rating")[:3]

        context["recommended_games"] = recommended_games
        context["top_games"] = top_games

        return context


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
