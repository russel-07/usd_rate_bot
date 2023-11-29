from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, UserRequest, TemplateText


class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'firstname', 'lastname', 'username',
                    'notification', 'reg_date')
    empty_value_display = '-пусто-'


class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'rate', 'date')
    list_filter = ('user', 'date')
    empty_value_display = '-пусто-'


class TemplateTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'text', 'slug')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(TemplateText, TemplateTextAdmin)
admin.site.unregister(Group)
