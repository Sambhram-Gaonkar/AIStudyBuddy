from django.urls import path

from . import views

app_name = 'summaries'

urlpatterns = [
    path('', views.summary_list, name='list'),
    path('generate/', views.generate_summary_view, name='generate'),
    path('<int:pk>/', views.summary_detail, name='detail'),
]
