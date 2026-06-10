from django.urls import path

from . import views

app_name = 'rag'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
]
