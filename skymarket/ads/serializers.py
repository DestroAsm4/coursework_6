from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Ad, Comment
from users.models import User

from users.serializers import CurrentUserSerializer


# from users.serializers import ListUserSerializer


# from users.serializers import ListUserSerializer


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою

class CommentSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    author = SlugRelatedField(slug_field='id', queryset=User.objects.all())

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

class UserAdSerializer(ModelSerializer):

    author = CurrentUserSerializer()
    class Meta:
        model = User
        fields = ['phone']

class AdCreateSerializer(ModelSerializer):

    # author = UserAdSerializer(read_only=True)
    author = SlugRelatedField(slug_field='id', queryset=User.objects.all())
    # phone = author.
    # user = UserSerializer()
    # author = user

    # def create(self, validated_data):
    #     author = self.context['request'].ad
    #     ad = Ad.objects.create(
    #         author=,
    #         **validated_data
    #     )
    #     return comment



    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price', 'author']

#  'phone', 'description', 'author_first_name', 'author_last_name', 'author_id'

class ListUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', "role", "email"]


