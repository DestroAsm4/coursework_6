# TODO здесь производится настройка пермишенов для нашего проекта
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from users.models import UserRoles

User = get_user_model()

class IsOwner(BasePermission):
    message = "Вы не можете редактировать чужие элементы"

    def has_object_permission(self, request, view, obj, *args, **kwargs):

        if hasattr(obj, "author"):
            owner = int(str(obj.author))
        else:
            raise Exception('Не подходящие данные')
        return owner == int(str(request.user))


class IsStaff(BasePermission):
    message = "Вы не админ"

    def has_object_permission(self, request, view, obj, *args, **kwargs):

        return request.user.role in [UserRoles.ADMIN]