from django.urls import path, include
from apps.User.views import RegisterView, LoginView, RetrieveView

app_name = 'User'

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path('login/', LoginView.as_view()),  # 登录  签发token
    # path('verify/', token_verify),  # 验证token 是否有效
    path("retrieve/", RetrieveView.as_view()),

]
