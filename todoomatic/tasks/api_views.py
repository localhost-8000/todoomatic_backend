
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from todoomatic.boards.models import Board

from todoomatic.tasks.models import AssignTask, Task
from todoomatic.tasks.serializers import AssignTaskSerializer, TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        board_id = self.kwargs["board_id"]
        return Task.objects.filter(pk=board_id)

    def perform_create(self, serializer):
        board_id = self.kwargs["board_id"]
        board = Board.objects.get(pk=board_id)
        serializer.save(board=board)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class AssignTaskViewSet(ModelViewSet):
    queryset = AssignTask.objects.all()
    serializer_class = AssignTaskSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        task = self.kwargs["task_id"]
        return AssignTask.objects.filter(task=task, deleted=False)

    def perform_create(self, serializer):
        task = self.kwargs["task_id"]
        user = self.kwargs["user_id"]
        serializer.save(task=task, user=user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
