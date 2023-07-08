from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from .models import Ad, Comment
from .serializers import AdSerializer, CommentSerializer, AdListSerializer

TOTAL_ON_PAGE = 10


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    queryset = Ad.objects.order_by('title')
    serializer_class = AdListSerializer

class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    serializers = {
        # "create": SelectionCreateSerializer
    }
    default_serializer = AdSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    @action(methods=['get'], detail=True)
    def comments(self, request, pk=None):
        commetns = Comment.objects.filter(ad_id=pk)
        print(commetns)
        return Response([commetn.serialize() for commetn in commetns])
    # permissions = {
    #     # 'list': [IsAuthenticated],
    #     'retrieve': [IsAuthenticated],
    #     'create': [IsAuthenticated],
    #     'update': [IsOwner],
    #     'destroy': [IsOwner],
    #     'partial_update': [IsOwner]

    # }
#
#
# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializers = {
#         # "create": SelectionCreateSerializer
#     }
#     default_serializer = CommentSerializer
#
#     def get_serializer_class(self):
#         return self.serializers.get(self.action, self.default_serializer)