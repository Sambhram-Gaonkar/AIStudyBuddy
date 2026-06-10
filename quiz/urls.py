from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_list, name='list'),
    path('generate/', views.generate_quiz_view, name='generate'),
    path('<int:pk>/', views.quiz_detail, name='detail'),
    path('<int:pk>/pdf/', views.export_quiz_pdf, name='pdf'),
]
