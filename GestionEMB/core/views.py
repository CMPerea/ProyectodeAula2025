from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import PerfilUsuario, AuditoriaLog
from .forms import LoginForm, CrearUsuarioForm, EditarUsuarioForm, EditarPerfilForm
from .utils import registrar_auditoria, get_client_ip, es_administrador


# ============= AUTENTICACIÓN =============

def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Verificar si el usuario está activo
                try:
                    perfil = user.perfil
                    if not perfil.activo:
                        messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
                        return render(request, 'login.html', {'form': form})
                except PerfilUsuario.DoesNotExist:
                    messages.error(request, 'Error en el perfil de usuario.')
                    return render(request, 'login.html', {'form': form})
                
                login(request, user)
                
                # Configurar sesión
                if not remember_me:
                    request.session.set_expiry(0)  # Expira al cerrar el navegador
                
                # Registrar en auditoría
                registrar_auditoria(
                    usuario=user,
                    accion='login',
                    entidad='usuario',
                    id_entidad=user.id,
                    descripcion=f'Inicio de sesión exitoso de {user.username}',
                    request=request
                )
                
                messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
                
                # Redirigir a la página solicitada o al dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """Vista de cierre de sesión"""
    # Registrar en auditoría
    registrar_auditoria(
        usuario=request.user,
        accion='logout',
        entidad='usuario',
        id_entidad=request.user.id,
        descripcion=f'Cierre de sesión de {request.user.username}',
        request=request
    )
    
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


# ============= DASHBOARD =============

@login_required
def homepage_view(request):
    """Vista principal del dashboard"""
    return render(request, 'homepage.html')


@login_required
def protocolo_view(request):
    """Vista de protocolos"""
    return render(request, 'protocolo.html')


# ============= GESTIÓN DE USUARIOS =============

@login_required
@user_passes_test(es_administrador, login_url='dashboard')
def listar_usuarios(request):
    """Lista todos los usuarios del sistema"""
    query = request.GET.get('q', '')
    rol_filter = request.GET.get('rol', '')
    estado_filter = request.GET.get('estado', '')
    
    usuarios = User.objects.select_related('perfil').all()
    
    # Filtros
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    if rol_filter:
        usuarios = usuarios.filter(perfil__rol=rol_filter)
    
    if estado_filter:
        if estado_filter == 'activo':
            usuarios = usuarios.filter(perfil__activo=True)
        elif estado_filter == 'inactivo':
            usuarios = usuarios.filter(perfil__activo=False)
    
    context = {
        'usuarios': usuarios,
        'query': query,
        'rol_filter': rol_filter,
        'estado_filter': estado_filter,
    }
    
    return render(request, 'usuarios/listar_usuarios.html', context)


@login_required
@user_passes_test(es_administrador, login_url='dashboard')
def crear_usuario(request):
    """Crear nuevo usuario"""
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            # Crear usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            
            # Crear perfil
            PerfilUsuario.objects.create(
                user=user,
                rol=form.cleaned_data['rol'],
                afiliacion=form.cleaned_data.get('afiliacion', ''),
                telefono=form.cleaned_data.get('telefono', ''),
                activo=True
            )
            
            # Registrar en auditoría
            registrar_auditoria(
                usuario=request.user,
                accion='crear',
                entidad='usuario',
                id_entidad=user.id,
                descripcion=f'Usuario {user.username} creado por {request.user.username}',
                request=request
            )
            
            # Enviar email de notificación (opcional)
            try:
                send_mail(
                    subject='Cuenta creada en Sistema EM&B',
                    message=f'''Hola {user.get_full_name()},

Tu cuenta ha sido creada exitosamente en el Sistema de Gestión EM&B.

Usuario: {user.username}
Email: {user.email}
Rol: {PerfilUsuario.objects.get(user=user).get_rol_display()}

Por favor cambia tu contraseña en el primer inicio de sesión.

Saludos,
Equipo EM&B''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error enviando email: {e}")
            
            messages.success(request, f'Usuario {user.username} creado exitosamente.')
            return redirect('listar_usuarios')
    else:
        form = CrearUsuarioForm()
    
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


@login_required
@user_passes_test(es_administrador, login_url='dashboard')
def editar_usuario(request, user_id):
    """Editar usuario existente"""
    usuario = get_object_or_404(User, id=user_id)
    perfil = usuario.perfil
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            # Actualizar usuario
            usuario = form.save()
            
            # Actualizar perfil
            perfil.rol = form.cleaned_data['rol']
            perfil.afiliacion = form.cleaned_data.get('afiliacion', '')
            perfil.telefono = form.cleaned_data.get('telefono', '')
            perfil.save()
            
            # Registrar en auditoría
            registrar_auditoria(
                usuario=request.user,
                accion='editar',
                entidad='usuario',
                id_entidad=usuario.id,
                descripcion=f'Usuario {usuario.username} editado por {request.user.username}',
                request=request
            )
            
            # Notificar al usuario (opcional)
            try:
                send_mail(
                    subject='Tu cuenta ha sido actualizada',
                    message=f'''Hola {usuario.get_full_name()},

Tu información de cuenta ha sido actualizada por un administrador.

Si no solicitaste este cambio, contacta al administrador.

Saludos,
Equipo EM&B''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[usuario.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error enviando email: {e}")
            
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente.')
            return redirect('listar_usuarios')
    else:
        # Pre-llenar el formulario con datos existentes
        initial = {
            'rol': perfil.rol,
            'afiliacion': perfil.afiliacion,
            'telefono': perfil.telefono,
        }
        form = EditarUsuarioForm(instance=usuario, initial=initial)
    
    return render(request, 'usuarios/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })


@login_required
@user_passes_test(es_administrador, login_url='dashboard')
def activar_desactivar_usuario(request, user_id):
    """Activar o desactivar un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    perfil = usuario.perfil
    
    # No permitir desactivar al propio usuario
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('listar_usuarios')
    
    # Cambiar estado
    perfil.activo = not perfil.activo
    perfil.save()
    
    accion_texto = 'activado' if perfil.activo else 'desactivado'
    
    # Registrar en auditoría
    registrar_auditoria(
        usuario=request.user,
        accion='editar',
        entidad='usuario',
        id_entidad=usuario.id,
        descripcion=f'Usuario {usuario.username} {accion_texto} por {request.user.username}',
        request=request
    )
    
    messages.success(request, f'Usuario {usuario.username} {accion_texto} exitosamente.')
    return redirect('listar_usuarios')


@login_required
@user_passes_test(es_administrador, login_url='dashboard')
def eliminar_usuario(request, user_id):
    """Eliminar un usuario (con confirmación)"""
    usuario = get_object_or_404(User, id=user_id)
    
    # No permitir eliminar al propio usuario
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('listar_usuarios')
    
    if request.method == 'POST':
        username = usuario.username
        
        # Registrar en auditoría antes de eliminar
        registrar_auditoria(
            usuario=request.user,
            accion='eliminar',
            entidad='usuario',
            id_entidad=usuario.id,
            descripcion=f'Usuario {username} eliminado por {request.user.username}',
            request=request
        )
        
        usuario.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente.')
        return redirect('listar_usuarios')
    
    return render(request, 'usuarios/confirmar_eliminar_usuario.html', {'usuario': usuario})


@login_required
def mi_perfil(request):
    """Ver y editar el perfil del usuario actual"""
    perfil = request.user.perfil
    
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            usuario = form.save()
            
            # Actualizar perfil
            perfil.telefono = form.cleaned_data.get('telefono', '')
            perfil.afiliacion = form.cleaned_data.get('afiliacion', '')
            perfil.save()
            
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('mi_perfil')
    else:
        initial = {
            'telefono': perfil.telefono,
            'afiliacion': perfil.afiliacion,
        }
        form = EditarPerfilForm(instance=request.user, initial=initial)
    
    return render(request, 'usuarios/mi_perfil.html', {'form': form, 'perfil': perfil})


@login_required
def cambiar_contrasena(request):
    """Cambiar contraseña del usuario actual"""
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión activa
            
            # Registrar en auditoría
            registrar_auditoria(
                usuario=request.user,
                accion='editar',
                entidad='usuario',
                id_entidad=request.user.id,
                descripcion=f'Contraseña cambiada por {request.user.username}',
                request=request
            )
            
            messages.success(request, 'Tu contraseña ha sido actualizada exitosamente.')
            return redirect('mi_perfil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'usuarios/cambiar_contrasena.html', {'form': form})


# ============= GESTIÓN DE ORGANISMOS =============

@login_required
def crear_organismo_view(request):
    return render(request, 'crear_organismo.html')

@login_required
def editar_organismo_view(request, organismo_id):
    return render(request, 'editar_organismo.html', {'organismo_id': organismo_id})

@login_required
def listar_organismos_view(request):
    return render(request, 'lista_organismos.html')    

@login_required
def detalle_organismo_view(request, organismo_id):
    return render(request, 'detalle_organismo.html', {'organismo_id': organismo_id})