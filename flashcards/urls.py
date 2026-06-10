from django.urls import path

from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.flashcard_list, name='list'),
    path('generate/', views.generate_flashcards_view, name='generate'),
    path('export/<int:note_id>/', views.export_flashcards_csv, name='csv'),
]
