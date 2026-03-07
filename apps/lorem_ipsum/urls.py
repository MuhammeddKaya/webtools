from django.urls import path
from . import views

app_name = 'lorem_ipsum'

urlpatterns = [
    path('', views.index, name='index'),
]
