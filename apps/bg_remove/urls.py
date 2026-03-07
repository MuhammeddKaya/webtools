from django.urls import path
from . import views

app_name = 'bg_remove'
urlpatterns = [
    path('', views.index, name='index'),
]
