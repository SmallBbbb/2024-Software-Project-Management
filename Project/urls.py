# myapp/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('homepage/', views.homepage, name='homepage'),
    path('test_standard/', views.test_standard, name='test_standard'),
    path('message/', views.message, name='message'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('admin/', views.admin_view, name='admin_view'),
    path('admin_standard/', views.admin_standard, name='admin_standard'),
    path('upload_standard/', views.upload_standard, name='upload_standard'),
    path('download_standard_template/', views.download_standard_template, name='download_standard_template'),
    path('download_project_template/', views.download_project_template, name='download_project_template'),
    path('standard/<int:standard_id>/projects/', views.standard_projects, name='standard_projects'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/upload_tutorial', views.upload_tutorial, name='upload_tutorial'),
    path('project/<int:project_id>/add_equipment', views.add_equipment, name='add_equipment'),
    path('<int:equipment_id>/show_equipment_detail', views.show_equipment_detail, name='show_equipment_detail'),
    path('project/<int:project_id>/add_sample', views.add_sample, name='add_sample'),
    path('project/<int:project_id>/download_regulation', views.download_regulation, name='download_regulation'),
    path('project/<int:project_id>/create_comparison', views.create_comparison, name='create_comparison'),
    path('<int:equipment_id>/start_comparison', views.start_comparison, name='start_comparison'),
    path('<int:equipment_id>/cancel_comparison', views.cancel_comparison, name='cancel_comparison'),




    # 可以添加更多的URL模式
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
