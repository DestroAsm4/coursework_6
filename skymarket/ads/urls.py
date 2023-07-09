from django.urls import path, include
from rest_framework import routers

from .views import AdListView, AdViewSet

# TODO настройка роутов для модели
# urlpatterns = [
# path('', AdListView.as_view()),
# ]
router = routers.SimpleRouter()
router.register(
    'ads',
    AdViewSet,
    basename='ads'

)
# router.register(
#     r'comments',
#     CommentViewSet,
#
# )
urlpatterns = router.urls