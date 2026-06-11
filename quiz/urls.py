from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_list, name='list'),
    path('generate/', views.generate_quiz_view, name='generate'),
    path('<int:pk>/', views.quiz_detail, name='detail'),
    path('<int:pk>/take/', views.take_quiz, name='take'),
    path('attempts/<int:pk>/', views.attempt_result, name='attempt_result'),
    path('<int:pk>/pdf/', views.export_quiz_pdf, name='pdf'),
]
