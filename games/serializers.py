from rest_framework.serializers import ModelSerializer

from games.models import Interaction


class InteractionSerializer(ModelSerializer):
    class Meta:
        model = Interaction
        fields = "__all__"
