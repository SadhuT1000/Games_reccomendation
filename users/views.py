from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, DetailView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.urls import reverse, reverse_lazy

from users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    """Делатьная информация по User"""
    model = User
    template_name = "users/profile.html"
    context_object_name = "users"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForme


    def get_success_url(self):
        return reverse("users:profile_user", args=[self.kwargs.get("pk")])


class UserCreateApiView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()



        """тут дописать оставшиеся дженерики для юсеров  and forms and serializrs"""