# GestionEMB/urls.py

# ... (keep your imports at the top) ...
from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- Autenticación y Vistas Principales ---
    path('', views.login_view, name='login'),
    path('dashboard/', views.homepage_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- Gestión de Organismos (Tus rutas existentes) ---
    path('organismos/crear/', views.crear_organismo_view, name='crear_organismo'),
    path('organismos/<int:organismo_id>/editar/', views.editar_organismo_view, name='editar_organismo'),
    path('organismos/', views.listar_organismos_view, name='listar_organismos'),
    path('organismos/<int:organismo_id>/', views.detalle_organismo_view, name='detalle_organismo'),
    
    # --- Gestión de Protocolos (Placeholder) ---
    path('protocolo/', views.protocolo_view, name='protocolo'),

    # --- Gestión de Usuarios (Nuevas rutas CORREGIDAS) ---
    # Usando los nombres de función que SÍ existen en core/views.py
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:user_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:user_id>/activar/', views.activar_desactivar_usuario, name='activar_desactivar_usuario'),
    path('usuarios/<int:user_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # --- Perfil de Usuario ---
    path('perfil/', views.mi_perfil, name='mi_perfil'),
    path('perfil/cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
]

# ... (keep your settings.DEBUG block at the bottom) ...
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)