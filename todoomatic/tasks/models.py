from django.contrib.auth import get_user_model
from django.db import models

from todoomatic.boards.models import Board

User = get_user_model()


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("In progress", "In Progress"),
    ("Done", "Done"),
    ("Cancelled", "Cancelled"),
)

PRIOTITY_CHOICES = (
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High"),
)


class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="Pending")
    priority = models.CharField(max_length=200, choices=PRIOTITY_CHOICES, default="Low")
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AssignTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.title
