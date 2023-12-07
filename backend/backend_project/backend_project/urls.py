from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('usd_rate_bot/admin/', admin.site.urls),
    path('usd_rate_bot/api/v1/', include('api_app.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
