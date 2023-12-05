from rest_framework import serializers

from .models import User, UserRequest, TemplateText


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['telegram_id', 'firstname', 'lastname', 'username',
                  'notification', 'reg_date']
        lookup_field = 'telegram_id'
        extra_kwargs = {
            'url': {'lookup_field': 'telegram_id'}
        }


class UserRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRequest
        fields = ['rate', 'date']


class TemplateTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateText
        fields = ['text']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
