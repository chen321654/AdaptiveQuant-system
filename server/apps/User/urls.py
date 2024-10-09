from django.urls import path, include
from apps.User.views import RegisterView, LoginView, RetrieveView, refresh_captcha


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path('captcha/', include('captcha.urls')),
    path('login/', LoginView.as_view()),  # 登录
    path('refresh_captcha/', refresh_captcha),
    # path('verify/', token_verify),  # 验证token 是否有效
    path("retrieve/", RetrieveView.as_view()),

]
