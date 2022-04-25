from rest_framework.serializers import ModelSerializer

from todoomatic.boards.models import Board
from todoomatic.users.api.serializers import UserSerializer


class BoardSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Board
        fields = "__all__"