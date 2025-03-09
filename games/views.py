from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, DetailView


class HomeView(TemplateView):
    """ Дормашняя страница"""
    template_name = 'games/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context