import os
import shutil

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
# views.py
from django.shortcuts import render,redirect
from django.contrib import messages


def index_view(request):
    if request.method == 'POST':
            if 'username' in request.POST and 'password' in request.POST:
                # 普通用户登录
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index_view')  # 重定向到登录后的页面
                else:
                    messages.error(request, '用户名或密码错误')
            elif 'admin_username' in request.POST and 'admin_password' in request.POST:
                # 管理员登录
                admin_username = request.POST['admin_username']
                admin_password = request.POST['admin_password']
                admin=authenticate(request,admin_username=admin_username,admin_password=admin_password)
                # 这里你可能需要自定义的验证逻辑，因为Django的authenticate默认不处理管理员

                if admin is not None:
                    # 处理管理员登录
                    login(request, admin)
                    # ...
                    return redirect('admin_view')  # 重定向到管理员登录后的页面
                else:
                    messages.error(request, '管理员用户名或密码错误')

                    # 如果不是POST请求，或者验证失败，显示表单
    return render(request, 'html/index.html')  # 确保这里的模板包含你的模态框
def admin_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/admin.html')
def comparison_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/comparison.html')
def device_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/device.html')
def exam_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/exam.html')
def message_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/message.html')
def project_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/project.html')
def project1_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/project1.html')
def regulations_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/regulations.html')
def sample_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/sample .html')
def standards_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/standards.html')
def training_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/training.html')