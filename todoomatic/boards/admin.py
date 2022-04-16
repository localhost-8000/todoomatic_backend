from django.contrib import admin

from todoomatic.boards.models import Board, BoardMember

admin.site.register(Board)
admin.site.register(BoardMember)