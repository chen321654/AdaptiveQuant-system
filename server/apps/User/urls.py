from django.urls import path, include
from apps.User.views import RegisterView
from rest_framework_simplejwt.views import token_obtain_pair, token_verify, token_refresh

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path('login/', token_obtain_pair),  # 登录  签发token
    path('verify/', token_verify),  # 验证token 是否有效

]
