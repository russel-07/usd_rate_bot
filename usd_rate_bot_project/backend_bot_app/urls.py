from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignUp, UserRetrieve, UserRequestViewSet, UserNotification
from .views import TemplateTextViewSet, CurrentUsdRate, UserCurrentUsdRate
from .views import NotificationList, UserViewSet


router = DefaultRouter()
router.register('user', UserViewSet, basename='User')
router.register('template_text', TemplateTextViewSet, basename='Template')


urlpatterns = [
    path('auth/', SignUp.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserRetrieve.as_view(), name='user_data'),
    path('requests/', UserRequestViewSet.as_view(), name='user_requests'),
    path('notification/', UserNotification.as_view(), name='notification'),
    path('current_usd_rate/', CurrentUsdRate.as_view(), name='current_rate'),
    path('user_current_usd_rate/', UserCurrentUsdRate.as_view()),
    path('notification_list/', NotificationList.as_view()),
    path('', include(router.urls)),
]
