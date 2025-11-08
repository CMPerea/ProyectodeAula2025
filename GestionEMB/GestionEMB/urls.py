# GestionEMB/urls.py

from django.contrib import admin
from django.urls import path
from core import views

# Para ver las fotos de perfil en modo de desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- Autenticación y Vistas Principales ---
    path('', views.login_view, name='login'),
    path('dashboard/', views.homepage_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), # Añadida vista de logout
    
    # --- Gestión de Organismos (Tus rutas existentes) ---
    path('organismos/crear/', views.crear_organismo_view, name='crear_organismo'),
    path('organismos/<int:organismo_id>/editar/', views.editar_organismo_view, name='editar_organismo'),
    path('organismos/', views.listar_organismos_view, name='listar_organismos'),
    path('organismos/<int:organismo_id>/', views.detalle_organismo_view, name='detalle_organismo'),
    
    # --- Gestión de Protocolos (Placeholder) ---
    path('protocolo/', views.protocolo_view, name='protocolo'),

    # --- Gestión de Usuarios (Nuevas rutas) ---
    path('usuarios/', views.lista_usuarios_view, name='lista_usuarios'),
    path('usuarios/crear/', views.registrar_usuario_view, name='registrar_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario_view, name='editar_usuario'),
    path('usuarios/activar/', views.activar_desactivar_view, name='activar_desactivar'),
    path('usuarios/cambiar-rol/', views.cambiar_rol_view, name='cambiar_rol'),
]

# Necesario para ver las fotos de perfil subidas
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)