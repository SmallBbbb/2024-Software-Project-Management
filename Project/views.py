import os
import shutil

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest
# views.py
from django.shortcuts import render,redirect
from django.contrib import messages

from Project.forms import StandardForm, ProjectForm, SampleForm
from openpyxl import load_workbook
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from .models import Standard, Project


def index_view(request):
    ''''''
    if request.method == 'POST':
                 return redirect('standards_view')  # 假设您有一个名为 'dashboard_view' 的视图
    return render(request, 'html/index.html')  # 确保这里的模板路径是正确的
def admin_view(request):
    # 可以在这里处理一些数据或逻辑
    return render(request, 'html/admin.html')



def admin_standard(request):
    # 获取所有标准
    standards = Standard.objects.all()

    # 将标准数据传递到模板
    return render(request, 'admin_standard.html', {'standards': standards})


from openpyxl import load_workbook

def upload_standard(request):
    error_message = None

    # 处理文件上传
    if request.method == 'POST' and request.FILES.get('standard_file'):
        uploaded_file = request.FILES['standard_file']
        print(f"Uploaded file: {uploaded_file.name}")

        # 验证文件类型
        if not uploaded_file.name.endswith('.xlsx'):
            error_message = "只支持上传 .xlsx 格式的文件"
        else:
            try:
                # 加载Excel文件
                wb = load_workbook(uploaded_file)
                sheet = wb.active
                print("Excel file loaded successfully.")

                # 检查前几行数据
                for row in sheet.iter_rows(min_row=2, max_row=5, values_only=True):
                    print(f"Row data: {row}")  # 输出前几行数据，确保它们符合预期

                # 假设Excel中的数据从第二行开始，第一行是标题
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    # 仅取前5列数据
                    row = row[:5]

                    # 过滤掉空行
                    if all(cell is None for cell in row):
                        continue  # 跳过空行

                    # 如果某个字段是空的，则跳过此行
                    if None in row:
                        print(f"Skipping row due to missing values: {row}")
                        continue

                    broad_category, category, project, standard_name, standard_number = row
                    print(f"Processing row: {broad_category}, {category}, {project}, {standard_name}, {standard_number}")

                    # 在数据库中创建新标准
                    Standard.objects.create(
                        BroadCategory=broad_category,
                        Category=category,
                        Project=project,
                        StandardName=standard_name,
                        StandardNumber=standard_number,
                    )

                print("File processed successfully.")
                return redirect('admin_standard')

            except Exception as e:
                error_message = f"文件处理出错: {e}"

    # 获取所有标准
    standards = Standard.objects.all()

    return render(request, 'admin_standard.html', {'standards': standards, 'error_message': error_message})


def standard_projects(request, standard_id):
    # 获取标准对象
    standard = get_object_or_404(Standard, id=standard_id)

    # 获取该标准下的所有项目
    projects = Project.objects.filter(standard=standard)

    if request.method == 'POST' and request.FILES.get('project_file'):
        uploaded_file = request.FILES['project_file']

        # 验证文件类型
        if not uploaded_file.name.endswith('.xlsx'):
            error_message = "只支持上传 .xlsx 格式的文件"
        else:
            try:
                # 加载 Excel 文件
                wb = load_workbook(uploaded_file)
                sheet = wb.active

                # 假设 Excel 中的数据从第二行开始，第一行是标题
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    # 获取 Excel 行数据
                    broad_category, category, name, standard_name, standard_number, clause_number = row

                    # 验证数据是否完整（可根据需要调整）
                    if not all([broad_category, category, name, standard_name, standard_number, clause_number]):
                        continue  # 跳过不完整的行

                    # 在数据库中创建新项目（Project）
                    Project.objects.create(
                        BroadCategory=broad_category,
                        Category=category,
                        Project=name,
                        StandardName=standard_name,
                        StandardNumber=standard_number,
                        ClauseNumber=clause_number,
                        Staff='',
                        Equipment='',
                        Procedure='',
                        Sample='',
                    )

                # 提示成功信息
                messages.success(request, '文件上传成功，项目数据已导入。')
                return redirect('standard_projects')  # 上传成功后跳转到标准页面

            except Exception as e:
                error_message = f"文件处理出错: {e}"

        # 获取所有项目数据
    projects = Project.objects.all()

    # 渲染模板，传递标准、项目
    return render(request, 'standard_projects.html', {
        'standard': standard,
        'projects': projects,
    })