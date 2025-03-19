# flake8: noqa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from games.models import Interaction
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User
from users.serializers import UserRetrieveSerializer, UserSerializer


class UserCreateApiView(CreateAPIView):
    """Создание пользователя через  CreateAPIView."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """Реализация представления просмотра пользователя, через RetrieveAPIView."""

    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserDetailView(LoginRequiredMixin, DetailView):
    """Делатьная информация по User"""

    model = User
    template_name = "users/profile.html"
    context_object_name = "users"

    model = Interaction
    template_name = "user_profile.html"
    context_object_name = "interactions"

    def get_queryset(self):
        return Interaction.objects.filter(user=self.request.user, is_favorite=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["favorite_games"] = self.get_queryset()
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["email", "phone", "avatar", "preferred_genres"]
    template_name = "profile_form.html"
    success_url = reverse_lazy("user_profile")


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     """Изменение данных пользователя"""
#     model = User
#     form_class = UserUpdateForm
#     def get_success_url(self):
#         return reverse("users:profile_user", args=[self.kwargs.get("pk")])


class UserCreateView(CreateView):
    """Регистрация пользователя"""

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")


# class LoginUserView(LoginView):
#     form_class = UserLoginForm
#     template_name = 'users/login.html'
