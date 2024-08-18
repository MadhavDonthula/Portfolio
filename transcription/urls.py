from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path("flashcards", views.flashcard_sets, name="flashcard_sets"),  # View all flashcard sets
    path("flashcards/<int:set_id>/", views.flashcards, name="flashcards"),  # View flashcards in a specific set
    path("check_pronunciation/", views.check_pronunciation, name="check_pronunciation"),  # Check pronunciation
    path("teacher_login", admin.site.urls, name="teacher_login"),
    path('assignments/<int:assignment_id>/', views.index, name='index'),
    path("record/<int:assignment_id>/", views.record_audio, name="record_audio"),
    path("save_audio/", views.save_audio, name="save_audio"),
    path('recording/<int:assignment_id>/<int:question_id>/', views.recording, name="recording"),
]
