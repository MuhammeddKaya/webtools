from django.urls import path
from . import views

app_name = 'pdf_split'
urlpatterns = [
    path('', views.index, name='index'),
    path('preview/', views.preview, name='preview'),
]
