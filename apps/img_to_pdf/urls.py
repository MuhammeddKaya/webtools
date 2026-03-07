from django.urls import path
from . import views

app_name = 'img_to_pdf'
urlpatterns = [
    path('', views.index, name='index'),
]
