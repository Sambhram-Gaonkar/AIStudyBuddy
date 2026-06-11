from django.urls import path

from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.flashcard_list, name='list'),
    path('generate/', views.generate_flashcards_view, name='generate'),
    path('revise/<int:note_id>/', views.revise_flashcards, name='revise'),
    path('export/<int:note_id>/', views.export_flashcards_csv, name='csv'),
]
