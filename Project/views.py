import os
import shutil

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest
# views.py
from django.shortcuts import render,redirect
from django.contrib import messages

from Project.forms import StandardForm, ProjectForm, SampleForm


def index_view(request):
    ''''''
    if request.method == 'POST':
         # # 检查是普通用户登录还是管理员登录
         # if 'username' in request.POST and 'password' in request.POST:
         #     # 普通用户登录
         #     username = request.POST['username']
         #     password = request.POST['password']
         #     user = authenticate(request, username=username, password=password)
         #     if user is not None:
         #         login(request, user)
         #         # 重定向到用户仪表板或其他页面
                 return redirect('standards_view')  # 假设您有一个名为 'dashboard_view' 的视图
         #     else:
         #        messages.error(request, '用户名或密码错误')
         #         # 注意：通常不建议在同一个表单中处理管理员和普通用户登录
         # # 但如果您确实需要这样做，请确保有适当的安全措施
         # # 例如，通过检查请求中的某个隐藏字段或使用不同的表单
         # elif 'admin_username' in request.POST and 'admin_password' in request.POST:
         #     # 管理员登录（自定义逻辑）
         #     # 注意：这里应该使用标准的用户名和密码字段，并检查用户权限
         #     admin_username = request.POST['admin_username']
         #     admin_password = request.POST['admin_password']
         #     # 假设您有一个自定义的方法来检查管理员权限
         #     # user = check_admin_credentials(admin_username, admin_password)
         #     # 但在这里，我们使用标准的 authenticate 来模拟
         #     # 实际上，您应该根据用户组的权限或角色来处理
         #     user = authenticate(request, username=admin_username, password=admin_password)
         #     if user is not None and user.is_staff:  # 假设管理员是 is_staff 为 True 的用户
         #         login(request, user)
         #         # 重定向到管理员页面
         #         return redirect('admin_view')  # 假设您有一个名为 'admin_view' 的视图
         #     else:
         #         messages.error(request, '管理员用户名或密码错误')
         #
         #         # 如果不是POST请求，或者验证失败，显示表单
    return render(request, 'html/index.html')  # 确保这里的模板路径是正确的
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
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_view')  # 重定向到列表页面
    else:
        form = ProjectForm()

    from Project.models import Project
    projects = Project.objects.all()
    return render(request, 'html/project.html', {'form': form, 'projects': projects})
def project1_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/project1.html')
def regulations_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/regulations.html')
def sample_view(request):
    # 可以在这里处理一些数据或逻辑
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sample_view')  # 重定向到列表页面
    else:
        form = SampleForm()

    from Project.models import Sample
    samples = Sample.objects.all()
    return render(request, 'html/sample.html', {'form': form, 'samples': samples})
def standards_view(request):
        if request.method == 'POST':
            form = StandardForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('standards_view')  # 重定向到列表页面
        else:
            form = StandardForm()

        from Project.models import Standard
        standards = Standard.objects.all()
        return render(request, 'html/standards.html', {'form': form, 'standards': standards})


def training_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/training.html')
def learn_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/learn.html')