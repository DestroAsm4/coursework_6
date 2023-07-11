from sqlite3 import IntegrityError

from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, raise_errors_on_nested_writes, ListSerializer
from rest_framework.utils import model_meta

User = get_user_model()
# TODO Здесь нам придется переопределить сериалайзер, который использует djoser
# TODO для создания пользователя из за того, что у нас имеются нестандартные поля




class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user



    class Meta:
        ordering = ['-id']
        model = User
        fields = ['email', 'first_name', 'last_name', "password", "phone", 'image']


class CurrentUserSerializer(serializers.ModelSerializer):


    class Meta:
        ordering = ['-id']
        model = User
        fields = ['first_name', 'last_name', "phone", "id", 'email', 'image']


class ListUserSerializer(serializers.ModelSerializer):

    # child = None

    class Meta:
        ordering = ['-id']
        model = User
        fields = '__all__'