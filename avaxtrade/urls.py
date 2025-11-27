"""
URL configuration for avaxtrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from apiconfig.views import UserRecentTransactionListView, Withdrawal

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version='v1',
        description="Your API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def health_check(request):
    try:
        User = get_user_model()
        User.objects.exists()
        return HttpResponse("Render works Successful", content_type="text/plain", status=200)
    except Exception:
        return HttpResponse("db_error", content_type="text/plain", status=503)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apiconfig.urls')),
    path("api/withdraw/", Withdrawal.as_view(), name="withdraw"),
    path('ping/', health_check ),
    path('api/transactions/', UserRecentTransactionListView.as_view(), name='transaction'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
