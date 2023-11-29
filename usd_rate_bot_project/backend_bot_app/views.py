import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import views, viewsets, status, generics

from .models import User, TemplateText
from .serializers import UserSerializer, UserRequestSerializer
from .serializers import TemplateTextSerializer


class SignUp(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_id = request.data.get('telegram_id')
        f_name = request.data.get('firstname')
        l_name = request.data.get('lastname')
        u_name = request.data.get('username')
        user, _ = User.objects.get_or_create(telegram_id=tg_id,
                                             firstname=f_name,
                                             lastname=l_name,
                                             username=u_name)
        user.save()
        token = self.get_token_for_user(user)
        user.auth_token = token['access']
        user.save()
        return Response({'token': token})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'telegram_id'
    http_method_names = ('get')


class UserRetrieve(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserRetrieve(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserNotification(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = self.request.user
        user.notification = not user.notification
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRequestViewSet(generics.ListAPIView):
    serializer_class = UserRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.requests.all()


class UserCurrentUsdRate(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        serializer = UserRequestSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            if request.data:
                serializer.save(user=user)
                return Response(serializer.data, status.HTTP_201_CREATED)
            error = {"rate": ["Обязательное поле."]}
            return Response(error, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TemplateTextViewSet(viewsets.ModelViewSet):
    queryset = TemplateText.objects.all()
    serializer_class = TemplateTextSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    http_method_names = ('get', 'head')


class CurrentUsdRate(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url)
        usd_rate = response.json()['Valute']['USD']['Value']
        return Response({'usd_rate': usd_rate})


class NotificationList(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        notification_list = (User.objects.filter(notification=True)
                             .values('telegram_id'))
        notification_list = [int(*n.values()) for n in notification_list]
        return Response({'notification_list': notification_list})
