from django.urls import path, include
from apps.User.views import RegisterView, LoginView, RetrieveView, refresh_captcha, ChangePasswordView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path('captcha/', include('captcha.urls')),
    path('login/', LoginView.as_view()),  # 登录
    path('refresh_captcha/', refresh_captcha),
    path("retrieve/", RetrieveView.as_view()),
    path("update/", ChangePasswordView.as_view()),
]
