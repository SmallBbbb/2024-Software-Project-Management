# myapp/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('admin/', views.admin_view, name='admin_view'),
    path('admin_standard/', views.admin_standard, name='admin_standard'),
    path('upload_standard/', views.upload_standard, name='upload_standard'),
    path('download_standard_template/', views.download_standard_template, name='download_standard_template'),
    path('download_project_template/', views.download_project_template, name='download_project_template'),
    path('standard/<int:standard_id>/projects/', views.standard_projects, name='standard_projects'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/add_equipment', views.add_equipment, name='add_equipment'),
    path('<int:equipment_id>/show_equipment_detail', views.show_equipment_detail, name='show_equipment_detail'),


    # 可以添加更多的URL模式
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
