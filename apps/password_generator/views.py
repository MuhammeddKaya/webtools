from django.shortcuts import render

def index(request):
    return render(request, 'password_generator/index.html')
