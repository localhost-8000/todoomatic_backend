from rest_framework import serializers

from todoomatic.boards.serializers import BoardSerializer
from todoomatic.users.api.serializers import UserSerializer

from .models import AssignTask, Task


class TaskSerializer(serializers.ModelSerializer):
    board = BoardSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = "__all__"

    
class AssignTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = AssignTask
        fields = "__all__"
