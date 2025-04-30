from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Cериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = "__all__"


class UserRetrieveSerializer(ModelSerializer):
    """Cериализатор для просмотра пользователя."""

    class Meta:
        model = User
        fields = "__all__"
