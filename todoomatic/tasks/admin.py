from django.contrib import admin

from todoomatic.tasks.models import AssignTask, Task

admin.site.register(Task)
admin.site.register(AssignTask)