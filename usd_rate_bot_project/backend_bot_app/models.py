from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    notification = models.BooleanField('Оповещение', default=False)
    reg_date = models.DateTimeField('Дата регистрации', auto_now_add=True)

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        user = self.username if self.username else self.telegram_id
        return user

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-reg_date']


class UserRequest(models.Model):
    rate = models.CharField(max_length=100, verbose_name='Курс доллара')
    date = models.DateTimeField('Дата запроса', auto_now_add=True)
    user = models.ForeignKey(User, models.CASCADE, related_name='requests')

    class Meta:
        verbose_name = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователей'
        ordering = ['-date']


class TemplateText(models.Model):
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=100, verbose_name='Описание')
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'Текстовый шаблон'
        verbose_name_plural = 'Текстовые шаблоны'
        ordering = ['id']
