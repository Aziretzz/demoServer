from . import views
from django.urls import path
from .views import r_register, all_data, r_login, g_register, g_login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, )

urlpatterns = [
    path('', views.rg),
    path('register_restaurant/', r_register, name='register_restaurant'),
    path('login_restaurant/', r_login, name='login_restaurant'),
    path('all_users/', all_data, name='all_users'),
    path('register_guest/', g_register, name='register_guest'),
    path('login_guest/', g_login, name='login_guest'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
