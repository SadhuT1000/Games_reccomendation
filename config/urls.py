
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("games/", include("games.urls", namespace="games")),
    # path("users/", include("users.urls", namespace="users")),
]
