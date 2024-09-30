import json
import re
import string
import random
import time

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from apps.User.models import User

# 注册视图
class RegisterView(View):
    def post(self, request):
        # 1.接收参数
        json_dict = json.loads(request.body)
        username = json_dict.get('username')
        password = json_dict.get('password')
        password_v = json_dict.get('password_v')

        # 2.验证参数
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不符合要求'})
        if password != password_v:
            return JsonResponse({'code': 400, 'errmsg': '两次输入的密码不相同'})

        # 3.数据入库
        try:
            # 加判断用户名是否存在？
            user = User.objects.create_user(username=username, password=password)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})

        return JsonResponse({'code': 200, 'msg': '注册成功'})

# 登录视图
class LoginView(View):
    pass

# 忘记密码视图
# t
class RetrieveView(View):
    def post(self, request):
        json_dict = json.loads(request.body)
        email = json_dict.get('email')

        try:
            user = User.objects.get(email=email)
            print(email)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '邮箱不存在'})

        captcha = SendCaptcha(email)
        cache.set('captcha', captcha, timeout=60*2)

        return JsonResponse({'code': 200})

    def get(self, request):
        captcha = cache.get('captcha')
        if captcha is None:
            return JsonResponse({"code": 400, "errmsg": "验证码已过期，请重试"})

        json_dict = json.loads(request.body)
        vcode = json_dict.get('vcode')

        if vcode != captcha:
            return JsonResponse({'code': 400, "errmsg": "验证码错误"})
        return JsonResponse({'code': 200, 'msg': "验证码正确"})


# 发送验证码
def SendCaptcha(email):
    captcha = "".join(random.sample(string.ascii_letters + string.digits, 8))
    title = "找回密码验证码"
    msg = f'您的验证码为：{captcha}，有效时间为2分钟。'
    send_mail(title, message=msg, recipient_list=[email], from_email=None)
    print("邮件发送成功！")
    return captcha
