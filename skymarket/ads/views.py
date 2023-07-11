from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
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
        # image = request.data['image']
        # if not request.data['image']:
        #     request.data.pop('image')
        result = super().create(request, *args, **kwargs)
        # if request.data['image']:
        # else:
        #     request.data['image'] = ''
        # print(request.data['image'])
        print(result.data)
        response = {
            "pk": result.data['pk'],
            "image": result.data['image'],
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
        results = [ad.serialize() for ad in ads]

        page = self.paginate_queryset(results)
        print(page)
        if page is not None:
            # serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(page)

        return Response(results)

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


        page = self.paginate_queryset(results)
        if page is not None:
            # serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(results)

        # serializer = self.get_serializer(results, many=True)
        return Response(results)

    @action(methods=['GET', 'PATCH', 'DELETE', 'POST'], detail=True, url_path='comments/(?P<comment_id>[^/.]+)')
    def comments_get_id(self, request, comment_id, pk=None, *args, **kwargs):

        if request.method == 'POST':
            comment = Comment()
            user = request.user
            comment.text = request.data['text']
            res = comment.save()
            print(res)
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

            return Response(result)



        if request.method == 'GET':
            comment = Comment.objects.get(pk=comment_id)
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

            return Response(result)

        if request.method == 'PATCH':

            data = request.data
            comment = Comment.objects.get(pk=comment_id)
            user = User.objects.get(pk=int(comment.serialize()['author']))
            comment.text = data['text']
            comment.save()

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

            return Response(result)


        if request.method == 'DELETE':
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return Response()



    # @action(methods=['PATCH'], detail=True, url_path='comments/(?P<comment_id>[^/.]+)')
    # def comments_update_id(self, request, comment_id, pk=None, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #     data = json.loads(request.body)
    #     self.object.name = data.get('text')
    #     self.object.save()
    #     comment = Comment.objects.get(pk=comment_id)
    #     user = User.objects.get(pk=int(comment.serialize()['author']))
    #     result = {
    #         'pk': comment.pk,
    #         'text': comment.text,
    #         'author_id': user.pk,
    #         'created_at': comment.created_at,
    #         "author_first_name": user.first_name,
    #         "author_last_name": user.last_name,
    #         "ad_id": comment.ad.pk,
    #         "author_image": user.image.name
    #     }

        # return Response(result)
    # permissions = {
    #     # 'list': [IsAuthenticated],
    #     'retrieve': [IsAuthenticated],
    #     'create': [IsAuthenticated],
    #     'update': [IsOwner],
    #     'destroy': [IsOwner],
    #     'partial_update': [IsOwner]

    # }

class UserAdsListAPIView(A)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializers = {
        # "create": SelectionCreateSerializer
    }
    default_serializer = CommentSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)