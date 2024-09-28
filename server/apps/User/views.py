import json
import re

from django.http import JsonResponse, HttpResponse
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
            return JsonResponse({'code': 400, 'msg': '缺少参数'})
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不符合要求'})
        if password != password_v:
            return JsonResponse({'code': 400, 'errmsg': '两次输入的密码不相同'})

        # 3.数据入库
        try:
            user = User.objects.create_user(username=username, password=password)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})

        return JsonResponse({'code': 200, 'msg': '注册成功'});


