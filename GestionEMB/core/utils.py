from .models import AuditoriaLog


def get_client_ip(request):
    """Obtener la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrar_auditoria(usuario, accion, entidad, id_entidad, descripcion, request, datos_adicionales=None):
    """
    Registrar una acción en el log de auditoría
    
    Args:
        usuario: Usuario que realiza la acción
        accion: Tipo de acción (crear, editar, eliminar, etc.)
        entidad: Tipo de entidad afectada
        id_entidad: ID de la entidad
        descripcion: Descripción de la acción
        request: Objeto request de Django
        datos_adicionales: Dict con información adicional (opcional)
    """
    try:
        AuditoriaLog.objects.create(
            usuario=usuario,
            accion=accion,
            entidad=entidad,
            id_entidad=id_entidad,
            descripcion=descripcion,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
            datos_adicionales=datos_adicionales
        )
    except Exception as e:
        print(f"Error registrando auditoría: {e}")


def es_administrador(user):
    """
    Verificar si el usuario es administrador
    
    Args:
        user: Usuario a verificar
        
    Returns:
        bool: True si es administrador, False en caso contrario
    """
    try:
        return user.perfil.rol == 'administrador'
    except:
        return False


def puede_editar_usuario(user, target_user):
    """
    Verificar si un usuario puede editar a otro
    
    Args:
        user: Usuario que intenta editar
        target_user: Usuario objetivo
        
    Returns:
        bool: True si puede editar, False en caso contrario
    """
    # El administrador puede editar a cualquiera
    if es_administrador(user):
        return True
    
    # Un usuario puede editar su propio perfil
    if user == target_user:
        return True
    
    return False


def generar_codigo_organismo(tipo):
    """
    Generar código único para organismo
    
    Args:
        tipo: Tipo de organismo (actinobacteria, levadura, hongo_filamentoso)
        
    Returns:
        str: Código generado
    """
    from .models import Organismo
    
    prefijos = {
        'actinobacteria': 'ACT',
        'levadura': 'LEV',
        'hongo_filamentoso': 'HON'
    }
    
    prefijo = prefijos.get(tipo, 'ORG')
    
    # Obtener el último código del mismo tipo
    ultimo = Organismo.objects.filter(tipo=tipo).order_by('-codigo').first()
    
    if ultimo and ultimo.codigo.startswith(f'EMB-{prefijo}-'):
        try:
            numero = int(ultimo.codigo.split('-')[-1])
            nuevo_numero = numero + 1
        except:
            nuevo_numero = 1
    else:
        nuevo_numero = 1
    
    return f'EMB-{prefijo}-{nuevo_numero:03d}'