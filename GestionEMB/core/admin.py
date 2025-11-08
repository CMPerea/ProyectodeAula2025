# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

# Unregister the default User admin
admin.site.unregister(User)

class PerfilUsuarioInline(admin.StackedInline):
    """
    Configuración para mostrar el PerfilUsuario dentro del admin de User.
    """
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    """
    Configuración personalizada para el admin de User,
    incluyendo el PerfilUsuarioInline.
    """
    inlines = (PerfilUsuarioInline, )
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'get_rol', 
        'get_activo'
    )
    list_select_related = ('perfil',)

    @admin.display(description='Rol', ordering='perfil__rol')
    def get_rol(self, obj):
        if hasattr(obj, 'perfil'):
            return obj.perfil.get_rol_display()
        return None

    @admin.display(description='Estado', ordering='perfil__activo', boolean=True)
    def get_activo(self, obj):
        if hasattr(obj, 'perfil'):
            return obj.perfil.activo
        return False

# Register the User model with our custom admin
admin.site.register(User, CustomUserAdmin)

# Opcional: Registrar otros modelos para verlos en el admin
from .models import Protocolo, Organismo, Equipo, Categoria, AuditoriaLog

admin.site.register(Protocolo)
admin.site.register(Organismo)
admin.site.register(Equipo)
admin.site.register(Categoria)
admin.site.register(AuditoriaLog)