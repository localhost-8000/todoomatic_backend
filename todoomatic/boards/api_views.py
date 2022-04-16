from rest_framework.viewsets import ModelViewSet

from todoomatic.boards.serializers import BoardSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import Board, BoardMember


class BoardViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing boards.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_users = BoardMember.objects.filter(user=self.request.user)
        return Board.objects.filter(deleted=False, id__in=[b.board.pk for b in board_users])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("serializer: ", serializer)
        serializer.is_valid(raise_exception=True)
        board = Board.objects.create(
            name=serializer.data.get('name'),
            description=serializer.data.get('description'),
            created_by=request.user
        )
        BoardMember.objects.create(
            board=board,
            user=request.user,
            is_owner=True
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        board = self.get_object()
        Board.objects.filter(pk=board.pk).update(deleted=True)

    