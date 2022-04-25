
from rest_framework.viewsets import ModelViewSet

from todoomatic.boards.serializers import BoardSerializer
from rest_framework.permissions import IsAuthenticated

from .models import Board, BoardMember


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_users = BoardMember.objects.filter(user=self.request.user)
        return Board.objects.filter(deleted=False, id__in=[b.board.pk for b in board_users])

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        BoardMember.objects.create(
            is_owner=True,
            user=self.request.user, 
            board=serializer.instance, 
        )

    def perform_destroy(self, instance):
        instance.deleted = True 
        instance.save()

    