from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Ad, Comment


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
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    # author = UserAdSerializer()


    class Meta:
        model = Ad
        fields = '__all__'

class AdListSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
