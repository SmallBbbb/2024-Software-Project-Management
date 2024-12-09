import io
import os
import shutil

import openpyxl
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest
# views.py
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.fonts import Font

from .models import Standard, Project, TestStaff, Equipment, Sample, Regulation, Comparison, Tutorial


def index_view(request):
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

#下载可用于上传标准的模板.xlsx文件
def download_standard_template(request):
    # 创建一个新的工作簿和工作表
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "标准模板"

    # 在工作表中写入一些示例数据
    ws['A1'] = "broad_category"
    ws['B1'] = "category"
    ws['C1'] = "project"
    ws['D1'] = "standard_name"
    ws['E1'] = "standard_number"

    for cell in ws[1]:  # 第一行是列名
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

        # 自动调整列宽
    for column in ws.columns:
        max_length = 0
        column_width = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        column_width = (max_length + 2)  # +2 for some padding
        ws.column_dimensions[cell.column_letter].width = column_width

    # 使用 io.BytesIO 对象将工作簿保存到内存中
    excel_stream = io.BytesIO()
    wb.save(excel_stream)

    # 重置流的位置到开头，以便可以读取它
    excel_stream.seek(0)

    # 设置响应头
    response = HttpResponse(
        excel_stream,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="standard_template.xlsx"'

    # 关闭流（可选，因为 HttpResponse 会在发送完数据后自动关闭它）
    # excel_stream.close()

    return response
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

#下载可用于上传的项目模板文件(.xlsx)
def download_project_template(request):
    # 创建一个新的工作簿和工作表
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "项目模板"

    # 在工作表中写入一些示例数据
    ws['A1'] = "broad_category"
    ws['B1'] = "category"
    ws['C1'] = "project"
    ws['D1'] = "standard_name"
    ws['E1'] = "standard_number"
    ws['F1'] = "clause_number"

    for cell in ws[1]:  # 第一行是列名
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

        # 自动调整列宽
    for column in ws.columns:
        max_length = 0
        column_width = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        column_width = (max_length + 2)  # +2 for some padding
        ws.column_dimensions[cell.column_letter].width = column_width

    # 使用 io.BytesIO 对象将工作簿保存到内存中
    excel_stream = io.BytesIO()
    wb.save(excel_stream)

    # 重置流的位置到开头，以便可以读取它
    excel_stream.seek(0)

    # 设置响应头
    response = HttpResponse(
        excel_stream,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="project_template.xlsx"'

    # 关闭流（可选，因为 HttpResponse 会在发送完数据后自动关闭它）
    # excel_stream.close()

    return response
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
                print(f"Excel file loaded successfully. Sheet name: {sheet.title}")

                for row in sheet.iter_rows(min_row=2, values_only=True):
                    print(f"Row data: {row}")

                    # 检查数据是否完整
                    if None in row:
                        print(f"Skipping row with empty value: {row}")
                        continue

                    broad_category, category, name, standard_name, standard_number, clause_number = row

                    # 在这里通过 standard_id 获取 Standard 实例
                    try:
                        standard = Standard.objects.get(id=standard_id)
                    except Standard.DoesNotExist:
                        print(f"Standard with id {standard_id} does not exist. Skipping project creation.")
                        continue

                    try:
                        # 在数据库中创建新项目，并将其与正确的 Standard 关联
                        project = Project.objects.create(
                            Category=category,
                            Project=name,
                            StandardName=standard_name,
                            StandardNumber=standard_number,
                            ClauseNumber=clause_number,
                            standard=standard,  # 设置外键关联
                        )
                        Tutorial.objects.create(
                            Category=category,
                            Project=name,
                            StandardName=standard_name,
                            StandardNumber=standard_number,
                            ClauseNumber=clause_number,
                            project=project  # 设置外键关联
                        )
                        Equipment.objects.create(
                            Category=category,
                            Project=name,
                            StandardName=standard_name,
                            StandardNumber=standard_number,
                            ClauseNumber=clause_number,
                            project=project  # 设置外键关联
                        )
                        Comparison.objects.create(
                            Category=category,
                            Project=name,
                            StandardName=standard_name,
                            StandardNumber=standard_number,
                            ClauseNumber=clause_number,
                            project=project  # 设置外键关联
                        )
                        Regulation.objects.create(
                            BroadCategory=broad_category,
                            Category=category,
                            Project=name,
                            StandardName=standard_name,
                            StandardNumber=standard_number,
                            ClauseNumber=clause_number,
                            project=project  # 设置外键关联
                        )
                    except Exception as e:
                        print(f"Error occurred while creating project {name}: {e}")
                        # 记录错误并向用户展示错误消息
                        messages.error(request, f"创建项目 {name} 时出错: {e}")
                        continue  # 继续处理下一个项目

                # 提示成功信息
                messages.success(request, '文件上传成功，项目数据已导入。')

            except Exception as e:
                print(f"Error occurred while processing the file: {e}")
                # 记录文件处理错误
                messages.error(request, f"文件处理出错: {e}")

    # 获取所有项目数据
    projects = Project.objects.filter(standard=standard)

    # 渲染模板，传递标准、项目
    return render(request, 'standard_projects.html', {
        'standard': standard,
        'projects': projects,
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    equipments = Equipment.objects.filter(project_id=project_id)
    return render(request, 'project_detail.html', {'project': project,
                                                                        'equipments': equipments})

def add_equipment(request, project_id):
    error_message = None
    if request.method == 'POST' and request.FILES['equipment_photo']:
        equipment = request.POST.get('equipment_name')
        manufacturer = request.POST.get('equipment_manufacturer')
        photo = request.FILES['equipment_photo']
        detail = request.POST.get('equipment_detail')
        project = get_object_or_404(Project, id=project_id)
        print(f"{equipment}+{manufacturer}+{photo}+{detail}+{project_id}")
        try:
            newEquipment = Equipment.objects.create(
                Category=project.Category,
                Project=project.Project,
                StandardName=project.StandardName,
                StandardNumber=project.StandardNumber,
                ClauseNumber=project.ClauseNumber,
                Equipment=equipment,
                Manufacturer=manufacturer,
                Photo=photo,
                Detail=detail,
                project_id=project_id,
            )
            newEquipment.save()
        except Exception as e:
            print(f"Error occurred while creating project {equipment}: {e}")
            # 记录错误并向用户展示错误消息
            messages.error(request, f"创建项目 {equipment} 时出错: {e}")
    equipments = Equipment.objects.filter(project_id=project_id)
    return redirect("project_detail", {'equipments': equipments})
def show_equipment_detail(request, equipment_id):
    equipment_detail = get_object_or_404(Equipment, id=equipment_id)
    return render(request, {'equipment_detail': equipment_detail})