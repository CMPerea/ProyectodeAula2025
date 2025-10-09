from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def homepage_view(request):
    return render(request, 'homepage.html')

def protocolo_view(request):
    return render(request, 'protocolo.html')