from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("record/<int:assignment_id>/", views.record_audio, name="record_audio"),
    path("save_audio/", views.save_audio, name="save_audio"),
    path('recording/<int:assignment_id>/<int:question_id>/', views.recording, name="recording"),
]
