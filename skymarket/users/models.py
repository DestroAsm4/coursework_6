from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from django.db.models import TextChoices

from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserRoles:
    USER = 'user'
    ADMIN = 'admin'
    choices = (
        (USER, USER),
        (ADMIN, ADMIN)
    )


class User(AbstractBaseUser):
    # TODO переопределение пользователя.
    # TODO подробности также можно поискать в рекоммендациях к проекту

    USERNAME_FIELD = 'email'

    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40, unique=True)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER )
    image = models.ImageField(upload_to='avatar_image', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     self.set_password(raw_password=self.password)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.pk)

    def serialize(self):
        return {
            'phone': self.phone,
            'author_first_name': self.first_name,
            'author_last_name': self.last_name,
            'author_id': self.pk
        }

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



    # также для работы модели пользователя должен быть переопределен
    # менеджер объектов
    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER
