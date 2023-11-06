from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

urlpatterns = [
    path("signup/", views.UserRegister.as_view(), name="signup"),  # 이메일 회원가입
    path("login/", views.UserLogin.as_view(), name="login"),  # 이메일 로그인
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),  # 토큰 갱신
]
