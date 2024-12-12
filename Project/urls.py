# myapp/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('homepage/', views.homepage, name='homepage'),
    path('messages/', views.message, name='message'),
    path('test_standard/', views.test_standard, name='test_standard'),
    path('test_search_standard/', views.test_search_standard, name='test_search_standard'),
    path('test_search_project/<int:standard_id>/', views.test_search_project, name='test_search_project'),
    path('test_project/<int:standard_id>/', views.test_project, name='test_project'),
    path('test_detail/<int:project_id>/', views.test_detail, name='test_detail'),
    path('admin_message/', views.admin_message, name='admin_message'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('admin_standard/', views.admin_standard, name='admin_standard'),
    path('admin_search_standard/', views.admin_search_standard, name='admin_search_standard'),
    path('upload_standard/', views.upload_standard, name='upload_standard'),
    path('download_standard_template/', views.download_standard_template, name='download_standard_template'),
    path('download_project_template/', views.download_project_template, name='download_project_template'),
    path('standard/<int:standard_id>/projects/', views.standard_projects, name='standard_projects'),
    path('admin_search_project/<int:standard_id>', views.admin_search_project, name='admin_search_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/upload_tutorial', views.upload_tutorial, name='upload_tutorial'),
    path('project/<int:project_id>/delete_tutorial', views.delete_tutorial, name='delete_tutorial'),
    path('project/<int:project_id>/upload_blank_paper', views.upload_blank_paper, name='upload_blank_paper'),
    path('project/<int:project_id>/delete_paper', views.delete_paper, name='delete_paper'),
    path('project/<int:project_id>/add_equipment', views.add_equipment, name='add_equipment'),
    path('<int:equipment_id>/show_equipment_detail', views.show_equipment_detail, name='show_equipment_detail'),
    path('project/<int:project_id>/add_sample', views.add_sample, name='add_sample'),
    path('project/<int:project_id>/download_regulation', views.download_regulation, name='download_regulation'),
    path('project/<int:project_id>/create_comparison', views.create_comparison, name='create_comparison'),
    path('<int:project_id>/start_comparison', views.start_comparison, name='start_comparison'),
    path('<int:project_id>/cancel_comparison', views.cancel_comparison, name='cancel_comparison'),

    #以下为测试人员可见页面相关url
    path('<int:project_id>/join_in_comparison', views.join_in_comparison, name='join_in_comparison'),
    path('download_blank_paper/<int:paper_id>', views.download_blank_paper, name='download_blank_paper'),
    path('<int:project_id>/upload_paper', views.upload_paper, name='upload_paper'),

    # 可以添加更多的URL模式
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
