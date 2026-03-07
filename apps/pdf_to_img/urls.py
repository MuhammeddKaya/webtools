from django.urls import path
from . import views

app_name = 'pdf_to_img'
urlpatterns = [
    path('', views.index, name='index'),
]
