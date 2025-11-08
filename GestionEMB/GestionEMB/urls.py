"""
URL configuration for GestionEMB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.urls import include

urlpatterns = [
    path('homepage/', views.homepage_view, name='homepage'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', views.login_view, name='login'),
    path('dashboard/', views.homepage_view, name='dashboard'),

    ##Gestion de Organismos
    path('crear_organismo/', views.crear_organismo_view, name='crear_organismo'),
    path('editar_organismo/<int:organismo_id>/', views.editar_organismo_view, name='editar_organismo'),
    path('listar_organismos/', views.listar_organismos_view, name='listar_organismos'),
    path('detalle_organismo/<int:organismo_id>/', views.detalle_organismo_view, name='detalle_organismo'),  
    
    ###Gestion de Protocolos
    
    path('protocolo/', views.protocolo_view, name='protocolo'),
    path('listaProtocolos/', views.listaProtocolos, name= 'listaProtocolos')
]
