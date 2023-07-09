from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# TODO здесь необходимо подклюючит нужные нам urls к проекту




# обратите внимание, что здесь в роуте мы регистрируем ViewSet,
# который импортирован из приложения Djoser



urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/redoc-tasks/", include("redoc.urls")),
    path('api/', include('users.urls')),
    path('api/', include('ads.urls')),


]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

