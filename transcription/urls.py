from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_audio, name='index'),
    path('save_audio/', views.save_audio, name='save_audio'),
    path('set_reference_text/', views.set_reference_text, name='set_reference_text'),
]
