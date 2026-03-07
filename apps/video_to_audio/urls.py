from django.urls import path
from . import views

app_name = 'video_to_audio'

urlpatterns = [
    path('', views.index, name='index'),
]
