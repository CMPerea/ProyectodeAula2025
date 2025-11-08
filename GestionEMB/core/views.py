from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from .models import Protocolo, Organismo, Usuario, Categoria, ProtocoloArchivo
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Max
from django.http import HttpResponse

def login_view(request):
    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to protocolos list (listaProcolos) after successful login
            return redirect('listaProcolos')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def homepage_view(request):
    return render(request, 'lista_protocolos.html')

###Gestion de Organismos
def crear_organismo_view(request):
    """Mostrar y procesar el formulario de creación de Organismo.

    El formulario en la plantilla usa nombres de campo y aquí mapeamos
    los campos más importantes hacia el modelo `Organismo`.
    """
    if request.method == 'POST':
        # Mapear campos del formulario
        codigo = request.POST.get('codigo') or request.POST.get('codigo_identificacion')
        nombre = request.POST.get('nombre_cientifico')
        cepa = request.POST.get('cepa')
        tipo = request.POST.get('tipo')
        origen = request.POST.get('origen')
        caracteristicas = request.POST.get('descripcion_morfologica') or request.POST.get('caracteristicas_morfologicas')
        condiciones = request.POST.get('observaciones_cultivo') or request.POST.get('condiciones_cultivo')
        temp = request.POST.get('temperatura')
        ph = request.POST.get('ph')

        # Buscar/seleccionar creador (modelo Usuario)
        creador = None
        try:
            if hasattr(request, 'user') and request.user.is_authenticated:
                user_email = getattr(request.user, 'email', None)
                if user_email:
                    creador = Usuario.objects.filter(email=user_email).first()
                if not creador:
                    creador = Usuario.objects.filter(nombre=request.user.username).first()
            if not creador:
                creador = Usuario.objects.first()
        except Exception:
            creador = None

        if not creador:
            return render(request, 'crear_organismo.html', {
                'error': 'No hay un usuario (modelo Usuario) en la base de datos. Por favor cree al menos un Usuario antes de registrar organismos.'
            })

        organismo = Organismo(
            nombre_cientifico=nombre or '',
            cepa=cepa or '',
            codigo_identificacion=codigo or '',
            tipo=tipo or '',
            origen=origen or '',
            caracteristicas_morfologicas=caracteristicas or '',
            condiciones_cultivo=condiciones or '',
            creador=creador,
            activo=1,
            fecha_creacion=timezone.now(),
            fecha_actualizacion=timezone.now(),
        )

        # Asignar campos numéricos si vienen bien formados
        try:
            if temp:
                organismo.temperatura_optima = float(temp)
        except Exception:
            pass
        try:
            if ph:
                organismo.ph_optimo = float(ph)
        except Exception:
            pass

        organismo.save()

        # Redirigir a la lista de organismos si la ruta existe (nombre 'lista' en core/urls.py)
        try:
            return redirect('lista')
        except Exception:
            return render(request, 'crear_organismo.html', {'success': 'Organismo guardado correctamente.'})

    return render(request, 'crear_organismo.html')
def editar_organismo_view(request, organismo_id):
    return render(request, 'editar_organismo.html', {'organismo_id': organismo_id})
def listar_organismos_view(request):
    return render(request, 'lista_organismos.html')    
def detalle_organismo_view(request, organismo_id):
    return render(request, 'detalle_organismo.html', {'organismo_id': organismo_id})
###Gestion de Protocolos

def listaProtocolos(request):
    protocolos = Protocolo.objects.all()
    return render(request, "lista_protocolos.html", {'protocolos': protocolos})

def protocolo_view(request):
    """Mostrar y procesar el formulario de creación de Protocolo.

    Campos esperados en el formulario:
    - titulo, descripcion, procedimiento, materiales, estado, autor_id, categoria_id
    """
    # Obtener listas reales de la base de datos para poblar los selects
    usuarios = Usuario.objects.all()
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        procedimiento = request.POST.get('procedimiento')
        materiales = request.POST.get('materiales')
        estado = request.POST.get('estado')
        autor_id = request.POST.get('autor_id')
        categoria_id = request.POST.get('categoria_id')

        # Buscar autor y categoria
        autor = None
        categoria = None
        try:
            if autor_id:
                autor = Usuario.objects.filter(id_usuario=int(autor_id)).first()
        except Exception:
            autor = None
        try:
            if categoria_id:
                categoria = Categoria.objects.filter(id_categoria=int(categoria_id)).first()
        except Exception:
            categoria = None

        # Validaciones mínimas y construcción de contexto para re-renderizar el formulario
        missing = []
        if not titulo or not titulo.strip():
            missing.append('titulo')
        if not procedimiento or not procedimiento.strip():
            missing.append('procedimiento')
        if not estado:
            missing.append('estado')
        if not autor:
            missing.append('autor')
        if not categoria:
            missing.append('categoria')

        context = {
            'titulo': titulo,
            'descripcion': descripcion,
            'procedimiento': procedimiento,
            'materiales': materiales,
            'estado_val': estado,
            'autor_val': autor_id,
            'categoria_val': categoria_id,
            'missing': missing,
            'usuarios': usuarios,
            'categorias': categorias,
        }

        if missing:
            # Mapear claves técnicas a nombres amigables para el usuario
            labels = {
                'titulo': 'Título',
                'procedimiento': 'Procedimiento',
                'estado': 'Estado',
                'autor': 'Autor',
                'categoria': 'Categoría',
            }
            friendly = [labels.get(k, k) for k in missing]
            context['error'] = 'Faltan campos obligatorios: ' + ', '.join(friendly)
            return render(request, 'protocolo.html', context)

        protocolo = Protocolo(
            titulo=titulo,
            descripcion=descripcion or '',
            procedimiento=procedimiento,
            materiales=materiales or '',
            estado=estado,
            autor=autor,
            categoria=categoria,
            fecha_creacion=timezone.now(),
            fecha_actualizacion=timezone.now(),
        )
        protocolo.save()
        # Guardar archivos adjuntos (si se enviaron) y recolectar errores
        archivos = request.FILES.getlist('adjuntos')
        saved_files = []
        file_errors = []
        import logging
        logger = logging.getLogger(__name__)
        for f in archivos:
            try:
                pa = ProtocoloArchivo(
                    protocolo=protocolo,
                    archivo=f,
                    nombre_original=getattr(f, 'name', ''),
                    fecha_subida=timezone.now(),
                )
                pa.save()
                saved_files.append(pa.nombre_original or pa.archivo.name)
            except Exception as exc:
                # Loguear y acumular para mostrar al usuario
                logger.exception('Error guardando archivo para protocolo %s: %s', protocolo.id_protocolo, exc)
                file_errors.append(f"{getattr(f, 'name', 'archivo desconocido')}: {str(exc)}")

        if file_errors:
            # Si hubo errores al guardar archivos, re-renderizamos el formulario
            # mostrando los mensajes, sin perder los valores del formulario.
            usuarios = Usuario.objects.all()
            categorias = Categoria.objects.all()
            context.update({
                'usuarios': usuarios,
                'categorias': categorias,
                'success': 'Protocolo creado correctamente, pero hubo problemas al guardar algunos archivos.',
                'file_errors': file_errors,
                'saved_files': saved_files,
            })
            return render(request, 'protocolo.html', context)

        # Si todo salió bien con los archivos (o no se enviaron), redirigimos
        try:
            return redirect('listaProcolos')
        except Exception:
            return render(request, 'protocolo.html', {'success': 'Protocolo creado correctamente.'})
    # GET: renderizar plantilla con usuarios y categorias
    return render(request, 'protocolo.html', {
        'usuarios': usuarios,
        'categorias': categorias,
    })


def protocolo_detalle_view(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, pk=protocolo_id)
    archivos = ProtocoloArchivo.objects.filter(protocolo=protocolo)
    return render(request, 'protocolo_detalle.html', {
        'protocolo': protocolo,
        'archivos': archivos,
    })


def protocolo_editar_view(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, pk=protocolo_id)
    usuarios = Usuario.objects.all()
    categorias = Categoria.objects.all()
    archivos_existentes = ProtocoloArchivo.objects.filter(protocolo=protocolo)

    if request.method == 'POST':
        # actualizar campos básicos
        protocolo.titulo = request.POST.get('titulo') or protocolo.titulo
        protocolo.descripcion = request.POST.get('descripcion') or protocolo.descripcion
        protocolo.procedimiento = request.POST.get('procedimiento') or protocolo.procedimiento
        protocolo.materiales = request.POST.get('materiales') or protocolo.materiales
        protocolo.estado = request.POST.get('estado') or protocolo.estado
        # autor y categoria
        autor_id = request.POST.get('autor_id')
        categoria_id = request.POST.get('categoria_id')
        try:
            if autor_id:
                protocolo.autor = Usuario.objects.filter(id_usuario=int(autor_id)).first() or protocolo.autor
        except Exception:
            pass
        try:
            if categoria_id:
                protocolo.categoria = Categoria.objects.filter(id_categoria=int(categoria_id)).first() or protocolo.categoria
        except Exception:
            pass

        protocolo.fecha_actualizacion = timezone.now()
        protocolo.save()

        # agregar nuevos archivos si los hay
        nuevos = request.FILES.getlist('adjuntos')
        for f in nuevos:
            pa = ProtocoloArchivo(
                protocolo=protocolo,
                archivo=f,
                nombre_original=getattr(f, 'name', ''),
                fecha_subida=timezone.now(),
            )
            pa.save()

        return redirect('protocolo_detalle', protocolo_id=protocolo.id_protocolo)

    # GET: render form para editar
    context = {
        'protocolo': protocolo,
        'usuarios': usuarios,
        'categorias': categorias,
        'archivos': archivos_existentes,
    }
    return render(request, 'protocolo_editar.html', context)


def protocolo_eliminar_view(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, pk=protocolo_id)
    # eliminar archivos del storage
    archivos = ProtocoloArchivo.objects.filter(protocolo=protocolo)
    for a in archivos:
        try:
            if a.archivo and a.archivo.name:
                path = os.path.join(settings.MEDIA_ROOT, a.archivo.name)
                if os.path.exists(path):
                    os.remove(path)
        except Exception:
            pass
    archivos.delete()
    protocolo.delete()
    try:
        return redirect('listaProcolos')
    except Exception:
        return render(request, 'lista_protocolos.html', {'success': 'Protocolo eliminado.'})


def protocolo_archivo_eliminar_view(request, protocolo_id, archivo_id):
    protocolo = get_object_or_404(Protocolo, pk=protocolo_id)
    archivo = get_object_or_404(ProtocoloArchivo, pk=archivo_id, protocolo=protocolo)
    # eliminar archivo fisico
    try:
        if archivo.archivo and archivo.archivo.name:
            path = os.path.join(settings.MEDIA_ROOT, archivo.archivo.name)
            if os.path.exists(path):
                os.remove(path)
    except Exception:
        pass
    archivo.delete()
    return redirect('protocolo_editar', protocolo_id=protocolo.id_protocolo)


def registrar_usuario_view(request):
    """Registrar un nuevo usuario: crea un auth.User y una fila en el modelo `Usuario`.

    Nota: el modelo `Usuario` del proyecto usa `id_usuario` como PK (IntegerField).
    Aquí asignamos un id incremental (max+1) al insertar. Si tu BD tiene otra
    estrategia, ajústalo.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        rol = request.POST.get('rol') or 'usuario'
        estado = request.POST.get('estado')

        # Validaciones básicas
        if not username or not password or not email:
            return render(request, 'registrar_usuario.html', {'error': 'Username, email y password son obligatorios.'})

        # Crear usuario de Django (auth)
        try:
            django_user = User.objects.create_user(username=username, email=email, password=password)
        except Exception as exc:
            return render(request, 'registrar_usuario.html', {'error': f'Error creando usuario de autenticación: {exc}'})

        # Determinar nuevo id_usuario
        try:
            max_id = Usuario.objects.aggregate(Max('id_usuario'))['id_usuario__max'] or 0
            new_id = int(max_id) + 1
        except Exception:
            new_id = None

        # Crear registro en tabla Usuario (si es posible)
        try:
            if new_id is None:
                # Si no podemos determinar id incremental, intentamos dejar que la BD asigne (raro)
                usuario = Usuario(id_usuario=django_user.id, nombre=f"{nombre} {apellidos}", email=email, rol=rol, activo=1)
            else:
                usuario = Usuario(id_usuario=new_id, nombre=f"{nombre} {apellidos}", email=email, rol=rol, activo=1)
            usuario.save()
        except Exception as exc:
            # Si falla crear el modelo local, borra el django_user para no dejar inconsistencia
            django_user.delete()
            return render(request, 'registrar_usuario.html', {'error': f'Error creando registro de Usuario: {exc}'})

        # Guardar foto de perfil en MEDIA_ROOT/users/<id>/ si viene
        try:
            foto = request.FILES.get('foto_perfil')
            if foto:
                users_dir = os.path.join(settings.MEDIA_ROOT, 'users')
                os.makedirs(users_dir, exist_ok=True)
                filename = f'user_{usuario.id_usuario}{os.path.splitext(foto.name)[1]}'
                dest = os.path.join(users_dir, filename)
                with open(dest, 'wb+') as f:
                    for chunk in foto.chunks():
                        f.write(chunk)
        except Exception:
            # No bloquear el registro por fallo al guardar foto
            pass

        # Éxito: redirigir a la lista de protocolos o mostrar mensaje
        try:
            return redirect('listaProcolos')
        except Exception:
            return render(request, 'registrar_usuario.html', {'success': 'Usuario creado correctamente.'})

    # GET: mostrar formulario
    return render(request, 'registrar_usuario.html')

