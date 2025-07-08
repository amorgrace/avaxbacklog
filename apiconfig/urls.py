from django.urls import path
from .views import RegisterView
from .views import CustomLoginView, CustomLogoutView, ChangePassword
from dj_rest_auth.views import UserDetailsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('change-password/', ChangePassword.as_view(), name='change_password'),
]
