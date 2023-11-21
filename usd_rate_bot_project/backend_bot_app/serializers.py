from rest_framework import serializers

from .models import User, UserRequest, TemplateText


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['telegram_id', 'username', 'notification', 'reg_date']


class UserRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRequest
        fields = ['user', 'rate', 'date']


class TemplateTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateText
        fields = ['description', 'text']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
