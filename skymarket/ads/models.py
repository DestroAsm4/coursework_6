from django.conf import settings
from django.db import models

DATE_INPUT_FORMATS = ['%Y-%m-%d %H:%M:%S %Z%z']
class Ad(models.Model):
    # TODO добавьте поля модели здесь
    title = models.CharField(max_length=40)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    author = models.ForeignKey('user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Ad_image', blank=True, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Comment(models.Model):
    # TODO добавьте поля модели здесь
    text = models.CharField(max_length=350)
    author = models.ForeignKey('user', on_delete=models.CASCADE)
    ad = models.ForeignKey('ad', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': self.author,
            'created_at': self.created_at,

        }

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text