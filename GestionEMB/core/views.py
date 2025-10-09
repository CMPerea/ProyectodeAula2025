from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to homepage after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def homepage_view(request):
    return render(request, 'homepage.html')

def protocolo_view(request):
    return render(request, 'protocolo.html')