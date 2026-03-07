from django.shortcuts import render

def index(request):
    return render(request, 'lorem_ipsum/index.html')
