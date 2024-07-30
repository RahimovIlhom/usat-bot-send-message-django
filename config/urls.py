from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from home_app import views

schema_view = get_schema_view(
   openapi.Info(
      title="USAT bot API",
      default_version='v1',
      description="USAT bot message API",
      terms_of_service="",
      contact=openapi.Contact(email="ilhomjonpersonal@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticated,],
)

urlpatterns = [
    path('', include('home_app.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.custom_login, name='login'),
    path('docs/swagger<format>/', login_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    path('docs/swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('docs/redoc/', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
    path('api/v1/message/', include('telegram.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'home_app.views.custom_404'
handler500 = 'home_app.views.custom_500'
