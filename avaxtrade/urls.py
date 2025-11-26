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
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from apiconfig.views import UserRecentTransactionListView, Withdrawal


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
    path('api/transactions/', UserRecentTransactionListView.as_view(), name='transaction')
]
