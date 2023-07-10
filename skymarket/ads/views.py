from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .permissions import IsOwner, IsStaff


from .models import Ad, Comment
from .serializers import AdSerializer, CommentSerializer, AdListSerializer, AdCreateSerializer

User = get_user_model()

TOTAL_ON_PAGE = 10


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    queryset = Ad.objects.order_by('title')
    serializer_class = AdListSerializer

class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    # serializer_class = AdSerializer

    serializers = {
            'create': AdCreateSerializer
    }
    default_serializer = AdSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    permissions = {
        # 'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsOwner | IsStaff],
        'destroy': [IsOwner | IsStaff],
        'partial_update': [IsOwner | IsStaff]
    }
    default_permission = [AllowAny]

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}


        ad = Ad.objects.get(pk=serializer.data['pk'])
        user = User.objects.get(pk=int(str(ad.author)))

        result = {
            "pk": ad.pk,
            "image": serializer.data['image'],
            "title": serializer.data['title'],
            "price": serializer.data['price'],
            "phone": user.phone,
            "description": serializer.data['description'],
            "author_first_name": user.first_name,
            "author_last_name": user.last_name,
            "author_id": user.pk
        }

        return Response(result)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        ad = Ad.objects.get(pk=serializer.data['pk'])
        user = User.objects.get(pk=int(str(ad.author)))

        response = {
            "pk": ad.pk,
            "image": ad.image.name,
            "title": ad.title,
            "price": ad.price,
            "phone": user.phone,
            "description": ad.description,
            "author_first_name": user.first_name,
            "author_last_name": user.last_name,
            "author_id": user.pk
        }

        return Response(response)

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.pk
        result = super().create(request, *args, **kwargs)
        response = {
            "pk": result.data['pk'],
            "image": request.data['image'],
            "title": request.data['title'],
            "price": request.data['price'],
            "phone": request.user.phone,
            "description": request.data['description'],
            "author_first_name": request.user.first_name,
            "author_last_name": request.user.last_name,
            "author_id": request.data['author']
        }

        return Response(response)

    @action(methods=['GET'], detail=False)
    def me(self, request, *args, **kwargs):

        ads = Ad.objects.filter(author_id=request.user.pk)
        print([ad.serialize() for ad in ads])

        return Response([ad.serialize() for ad in ads])
        # return Response({'status': 'OK'})
    @action(methods=['GET'], detail=True)
    def comments(self, request, pk=None, *args, **kwargs):
        results = []

        comments = Comment.objects.filter(ad_id=pk)
        for comment in comments:
            user = User.objects.get(pk=int(comment.serialize()['author']))

            result = {
                'pk': comment.pk,
                'text': comment.text,
                'author_id': user.pk,
                'created_at': comment.created_at,
                "author_first_name": user.first_name,
                "author_last_name": user.last_name,
                "ad_id": comment.ad.pk,
                "author_image": user.image.name
            }
            results.append(result)


        return Response(results)
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
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializers = {
        # "create": SelectionCreateSerializer
    }
    default_serializer = CommentSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)