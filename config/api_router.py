from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from todoomatic.boards.api_views import BoardViewSet
from todoomatic.tasks.api_views import TaskViewSet

from todoomatic.users.api.views import CreateUser, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("auth", CreateUser)
router.register('boards', BoardViewSet, basename="boards_api")
router.register("boards/(?P<board_id>\d+)/tasks", TaskViewSet, basename="tasks_api")


app_name = "api"
urlpatterns = router.urls
