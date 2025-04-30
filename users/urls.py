# flake8: noqa
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from games.apps import GamesConfig
from users.views import UserCreateView, UserDetailView, UserUpdateView

app_name = GamesConfig.name

urlpatterns = [

    path(
        "login/", LoginView.as_view(template_name="users/user_form.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="profile_user"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
]
