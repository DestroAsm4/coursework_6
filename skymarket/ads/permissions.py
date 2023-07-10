# TODO здесь производится настройка пермишенов для нашего проекта


from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    message = "Вы не можете редактировать чужие элементы"

    def has_object_permission(self, request, view, obj):

        print(obj)

        if hasattr(obj, "owner"):
            owner = obj.owner
        elif hasattr(obj, "author"):
            owner = obj.author
        else:
            raise Exception('Не подходящие данные')
        return owner == request.user

class IsStaff(BasePermission):
    message = "Вы не админ"

    def has_object_permission(self, request, view, obj):
        return request.user.role in [UserRoles.ADMIN]