from django.urls import path
from . import views

app_name = 'text_tools'
urlpatterns = [
    path('', views.index, name='index'),
]
