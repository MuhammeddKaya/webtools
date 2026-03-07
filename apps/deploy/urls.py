from django.urls import path
from . import views

app_name = 'deploy'

urlpatterns = [
    path('webhook/', views.webhook_deploy, name='webhook'),
]
