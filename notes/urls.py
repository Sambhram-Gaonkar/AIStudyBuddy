from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='list'),
    path('upload/', views.upload_note, name='upload'),
    path('subjects/create/', views.create_subject, name='create_subject'),
    path('<int:pk>/', views.note_detail, name='detail'),
]
