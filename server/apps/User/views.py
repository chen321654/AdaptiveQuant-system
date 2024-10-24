import json
import re
import string
import random

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from apps.User.models import User
from utils.views import LoginRequiredJSONMixin


# 注册视图
class RegisterView(View):
    def post(self, request):
        # 1.接收参数
        json_dict = json.loads(request.body)
        username = json_dict.get('username')
        password = json_dict.get('password')
        password_v = json_dict.get('password_v')
        email = json_dict.get('email')
        email_code = json_dict.get('email_code')

        # 2.验证参数
        if not all([username, password]):
            return JsonResponse({'code': 400, 'msg': '缺少参数'})
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'msg': '用户名不符合要求'})
        if password != password_v:
            return JsonResponse({'code': 400, 'msg': '两次输入的密码不相同'})

        # 3.验证邮箱验证码
        email_captcha = cache.get('email_captcha')
        if email_captcha is None:
            return JsonResponse({"code": 400, "msg": "验证码已过期，请重试"})

        if email_code != email_captcha:
            return JsonResponse({'code': 400, "msg": "验证码错误"})

        # 4.数据入库
        try:
            # 加判断用户名是否存在？
            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'msg': '注册失败'})

        return JsonResponse({'code': 200, 'msg': '注册成功'})


# 登录视图
class LoginView(View):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        print(hashkey, image_url)
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return JsonResponse({"code": 200, "data": captcha})

    def post(self, request):
        json_dict = json.loads(request.body)
        username = json_dict.get('username')
        password = json_dict.get('password')
        captcha = json_dict.get('captcha')
        hashkey = json_dict.get('hashkey')
        if not all([username, password]):
            return JsonResponse({'code': 400, 'msg': '参数不全'})
        if not jarge_captcha(captcha, hashkey):
            return JsonResponse({'code': 400, 'msg': '验证码错误'})
        # 检验用户名与密码是否正确
        from django.contrib.auth import authenticate
        # authenticate参数为用户和密码，若用户密码正确，返回User信息，否则返回None
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'msg': '账号或密码错误'})
        # session
        from django.contrib.auth import login
        login(request, user)
        request.session.set_expiry(None)
        response = JsonResponse({'code': 200, 'msg': '登陆成功'})
        response.set_cookie('username', username)
        return response


# 忘记密码视图
class RetrieveView(View):
    def get(self, request):
        json_dict = json.loads(request.body)
        email = json_dict.get('email')

        try:
            user = User.objects.get(email=email)
            print(email)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'msg': '邮箱不存在'})

        email_captcha = SendCaptchaEmail(email)
        cache.set('email_captcha', email_captcha, timeout=60 * 2)

        return JsonResponse({'code': 200})


class ChangePasswordView(LoginRequiredJSONMixin, View):
    def put(self, request):
        # 接收参数
        json_dict = json.loads(request.body)
        password = json_dict.get('password')
        password_v = json_dict.get('password_v')

        # 校验数据
        if password != password_v:
            return JsonResponse({'code': 400, 'msg': '两次输入的密码不相同'})
        # 修改密码
        try:
            request.user.set_password(password)
            request.user.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '修改密码失败'})
        # 清理状态保持信息
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': '修改密码成功'})
        response.delete_cookie('username')
        return response


# 发送验证码
def SendCaptchaEmail(email):
    email_captcha = "".join(random.sample(string.ascii_letters + string.digits, 8))
    title = "找回密码验证码"
    msg = f'您的验证码为：{email_captcha}，有效时间为2分钟，请不要将验证码告知其他人。'
    send_mail(title, message=msg, recipient_list=[email], from_email=None)
    print("邮件发送成功！")
    return email_captcha


# 创建验证码
def captcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


# 刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            CaptchaStore.remove_expired()
            if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
                get_captcha.delete()
                return True
        except:
            return False
    else:
        return False
