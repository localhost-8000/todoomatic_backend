
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from todoomatic.tasks.models import AssignTask, Task

from .serializers import CreateUserSerializer, MinimalTaskSerializer, UserSerializer, UserSerializerWithToken

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=['get'])
    def tasks(self, request):
        user_tasks = AssignTask.objects.filter(user=request.user, deleted=False)
        pending_task_ids = []
        progress_task_ids = []
        done_task_ids = []
        for task in user_tasks:
            if task.task.status == 'Pending':
                pending_task_ids.append(task.task.id)
            elif task.task.status == 'In Progress':
                progress_task_ids.append(task.task.id)
            else:
                done_task_ids.append(task.task.id)
        
        pending = MinimalTaskSerializer(Task.objects.filter(pk__in=pending_task_ids), many=True).data
        progress = MinimalTaskSerializer(Task.objects.filter(pk__in=progress_task_ids), many=True).data
        done = MinimalTaskSerializer(Task.objects.filter(pk__in=done_task_ids), many=True).data

        return Response(status=status.HTTP_200_OK, data={
            "pending": pending,
            "progress": progress,
            "done": done
        })





@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            name=serializer.validated_data['name'],
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            photoURL=serializer.validated_data['photoURL']
        )
        user.set_password(user.password)
      
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        
        data = {
            "token": token.key
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
