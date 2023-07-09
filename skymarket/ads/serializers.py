from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Ad, Comment
from ..users.models import User

# from users.serializers import ListUserSerializer


# from users.serializers import ListUserSerializer


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою

class CommentSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    class Meta:
        model = Comment
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price', 'description']


class AdDetailSerializer(serializers.ModelSerializer):
    # author = UserAdSerializer()


    class Meta:
        model = Ad
        fields = '__all__'

class AdListSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class AdCreateSerializer(ModelSerializer):

    # author = ListUserSerializer()

    first_name = SlugRelatedField(slug_field='user.first_name', queryset=User.objects.all())


    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price', 'phone', 'description', 'author_first_name', 'author_last_name', 'author_id']



