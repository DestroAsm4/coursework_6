from django.urls import path, include
from rest_framework import routers

from .views import AdListView, AdViewSet, CommentViewSet

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
urlpatterns = router.urls




urlpatterns += ad_router.urls
# router.register(
#     r'comments',
#     CommentViewSet,
#     'comments'
#
# )
