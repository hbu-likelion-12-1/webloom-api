from django.urls import path
from .api import *


urlpatterns = [
    path("auth/signup", SignupAPI.as_view()),
    path("auth/kakao/url", KakaoRedirectAPI.as_view()),
    path("auth/kakao/login", KakaoLoginAPI.as_view()),
]
