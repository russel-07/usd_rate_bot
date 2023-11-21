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
        telegram_id = request.data.get('telegram_id')
        username = request.data.get('username')
        user, _ = User.objects.get_or_create(telegram_id=telegram_id,
                                             username=username)
        user.save()
        token = self.get_token_for_user(user)
        return Response({'token': token})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}


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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            error = {"rate": ["Обязательное поле."]}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        rate = response.json()['Valute']['USD']['Value']
        return Response({'usd_rate': rate})
