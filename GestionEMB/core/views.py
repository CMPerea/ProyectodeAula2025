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
###Gestion de Organismos
def crear_organismo_view(request):
    return render(request, 'crear_organismo.html')
def editar_organismo_view(request, organismo_id):
    return render(request, 'editar_organismo.html', {'organismo_id': organismo_id})
def listar_organismos_view(request):
    return render(request, 'listar_organismos.html')    
def detalle_organismo_view(request, organismo_id):
    return render(request, 'detalle_organismo.html', {'organismo_id': organismo_id})
###Gestion de Protocolos

