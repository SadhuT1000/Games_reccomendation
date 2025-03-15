from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, DetailView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from django.urls import reverse, reverse_lazy

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User
from users.serializers import UserSerializer, UserRetrieveSerializer


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


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение данных пользователя"""
    model = User
    form_class = UserUpdateForm
    def get_success_url(self):
        return reverse("users:profile_user", args=[self.kwargs.get("pk")])


class UserCreateView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')


# class LoginUserView(LoginView):
#     form_class = UserLoginForm
#     template_name = 'users/login.html'
