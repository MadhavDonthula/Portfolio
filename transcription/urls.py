from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("flashcards", views.blank, name="flashcards"),  # Home page where users input the class code
    path("speak", views.blank, name="speak"), 
    path("game", views.blank, name="game"),
    path("teacher_login", admin.site.urls, name="teacher_login"),
    path("contact_us", views.blank, name="contact_us"),
    path('assignments/<int:assignment_id>/', views.index, name='index'),  
    path("record/<int:assignment_id>/", views.record_audio, name="record_audio"),  # Record audio for specific assignment
    path("save_audio/", views.save_audio, name="save_audio"),  # Save the recorded audio
    path('recording/<int:assignment_id>/<int:question_id>/', views.recording, name="recording"),  # 
]
