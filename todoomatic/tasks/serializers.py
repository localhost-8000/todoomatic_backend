from rest_framework import serializers

from .models import AssignTask, Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"

    
class AssignTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignTask
        fields = "__all__"
