# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('admin/', views.admin_view, name='admin_view'),
    path('admin_standard/', views.admin_standard, name='admin_standard'),
    path('upload_standard/', views.upload_standard, name='upload_standard'),
    path('standard/<int:standard_id>/projects/', views.standard_projects, name='standard_projects'),


    # 可以添加更多的URL模式
]
