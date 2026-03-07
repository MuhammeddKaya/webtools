from django.urls import path
from . import views

app_name = "youtube_downloader"

urlpatterns = [
    path("", views.index, name="index"),
]

