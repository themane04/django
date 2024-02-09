from django.contrib import admin
from django.urls import path
from .views import note_list, create_note, update_note, delete_note

urlpatterns = [
    path('', note_list, name='note_list'),
    path('create/', create_note, name='create_note'),
    path('update/<int:pk>', update_note, name='update_note'),
    path('delete/<int:pk>', delete_note, name='delete_note')
]
