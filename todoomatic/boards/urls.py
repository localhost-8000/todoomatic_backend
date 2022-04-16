
from rest_framework.routers import SimpleRouter

from todoomatic.boards.api_views import BoardViewSet

router = SimpleRouter()

router.register(r'boards', BoardViewSet, basename="boards_api")


