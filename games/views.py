from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from games.models import Games, Interaction


class HomeView(TemplateView):
    """ Дормашняя страница"""

    template_name = 'games/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GamesDetailView(LoginRequiredMixin, DetailView):
    """Делатьная информация по игре"""
    model = Games
    template_name = "games/game.html"
    context_object_name = "games"

class StatisticInteractionView(LoginRequiredMixin, ListView):
    """Представление статистики рекомендаций для пользователя."""
    model = Interaction
    template_name = "games/statistic.html"
    context_object_name = "statistics"

    def get_queryset(self):
        return Interaction.objects.filter(user=self.request.user)


