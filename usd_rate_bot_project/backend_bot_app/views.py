import requests

from django.shortcuts import get_object_or_404
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import User, TemplateText
from .serializers import UserSerializer, UserRequestSerializer
from .serializers import TemplateTextSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ('get', 'post', 'patch')
    lookup_field = 'telegram_id'


class UserRequestViewSet(viewsets.ModelViewSet):
    serializer_class = UserRequestSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ('get', 'post')

    def get_queryset(self):
        user = get_object_or_404(User, telegram_id=self.kwargs.get('telegram_id'))
        return user.requests.all()

    def perform_create(self, serializer):
        user = get_object_or_404(User, telegram_id=self.kwargs.get('telegram_id'))
        serializer.save(user=user)


class TemplateTextViewSet(viewsets.ModelViewSet):
    queryset = TemplateText.objects.all()
    serializer_class = TemplateTextSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ('get')
    lookup_field = 'slug'


class NotifiedList(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        n_list = User.objects.filter(notification=True).values('telegram_id')
        n_list = [int(*n.values()) for n in n_list]
        return Response({'notified_list': n_list})


class UpdateUsdRate(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url)
        usd_rate = response.json()['Valute']['USD']['Value']
        return Response({'usd_rate': usd_rate})
