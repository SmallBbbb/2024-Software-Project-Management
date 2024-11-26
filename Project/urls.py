# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('admin/', views.admin_view, name='admin_view'),
    path('comparison/', views.comparison_view, name='comparison_view'),
    path('device/', views.device_view, name='device_view'),
    path('exam/', views.exam_view, name='exam_view'),
    path('message/', views.message_view, name='message_view'),
    path('project/', views.project_view, name='project_view'),
    path('project1/', views.project1_view, name='project1_view'),
    path('regulations/', views.regulations_view, name='regulations_view'),
    path('sample/', views.sample_view, name='sample_view'),
    path('standards/', views.standards_view, name='standards_view'),
    path('training/', views.training_view, name='training_view'),
    path('learn/', views.learn_view, name='learn_view'),
    # 可以添加更多的URL模式
]
