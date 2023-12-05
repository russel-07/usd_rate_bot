from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, UserRequestViewSet, TemplateTextViewSet
from .views import UpdateUsdRate, NotifiedList


router = DefaultRouter()
router.register('user', UserViewSet, basename='User')
router.register('user/(?P<telegram_id>[0-9]+)/requests',
                UserRequestViewSet, basename='UserRequest')
router.register('template_text', TemplateTextViewSet, basename='TemplateText')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notified_list/', NotifiedList.as_view(), name='notified_list'),
    path('rate/', UpdateUsdRate.as_view(), name='update_rate'),
    path('', include(router.urls)),
]
