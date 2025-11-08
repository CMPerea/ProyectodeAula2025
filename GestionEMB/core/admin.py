# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    """
    Configuración personalizada para el modelo Usuario en el admin de Django.
    """
    model = Usuario
    list_display = ('email', 'username', 'nombre', 'apellidos', 'rol', 'estado', 'is_staff')
    list_filter = ('rol', 'estado', 'is_staff', 'is_superuser', 'is_active')
    
    # Campos que se mostrarán en el formulario de edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'apellidos', 'telefono', 'foto_perfil')}),
        ('Información Laboral', {'fields': ('id_empleado', 'departamento', 'cargo', 'fecha_ingreso')}),
        ('Permisos y Estado', {'fields': ('rol', 'estado', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos para el formulario de creación de usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'nombre', 'apellidos', 'id_empleado', 'password', 'password2'),
        }),
    )
    
    search_fields = ('email', 'username', 'nombre', 'apellidos', 'id_empleado')
    ordering = ('email',)

# Registra tu modelo personalizado
admin.site.register(Usuario, UsuarioAdmin)