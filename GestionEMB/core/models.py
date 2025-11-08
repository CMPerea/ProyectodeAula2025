from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class PerfilUsuario(models.Model):
    """Extensión del modelo User para información adicional"""
    ROLES = [
        ('administrador', 'Administrador'),
        ('estudiante', 'Estudiante'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    afiliacion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_rol_display()}"


class Categoria(models.Model):
    """Categorías para clasificar protocolos"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Protocolo(models.Model):
    """Protocolos de investigación del laboratorio"""
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('en_revision', 'En Revisión'),
        ('validado', 'Validado'),
        ('obsoleto', 'Obsoleto'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    procedimiento = models.TextField()
    materiales = models.TextField(blank=True, null=True)
    referencias = models.TextField(blank=True, null=True)
    
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='protocolos')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='protocolos_creados')
    
    version = models.IntegerField(default=1)
    protocolo_padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='versiones')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    validado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='protocolos_validados')
    
    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['titulo', 'estado']),
            models.Index(fields=['categoria', 'estado']),
        ]
    
    def __str__(self):
        return f"{self.titulo} (v{self.version})"
    
    def crear_nueva_version(self, usuario):
        """Crea una nueva versión del protocolo"""
        nueva_version = Protocolo.objects.create(
            titulo=self.titulo,
            descripcion=self.descripcion,
            procedimiento=self.procedimiento,
            materiales=self.materiales,
            referencias=self.referencias,
            categoria=self.categoria,
            estado='borrador',
            autor=usuario,
            version=self.version + 1,
            protocolo_padre=self.protocolo_padre if self.protocolo_padre else self,
        )
        return nueva_version


class Organismo(models.Model):
    """Microorganismos registrados en el laboratorio"""
    TIPOS = [
        ('actinobacteria', 'Actinobacteria'),
        ('levadura', 'Levadura'),
        ('hongo_filamentoso', 'Hongo Filamentoso'),
    ]
    
    # Información taxonómica
    codigo = models.CharField(max_length=50, unique=True, help_text="Código único del laboratorio (ej: EMB-ACT-001)")
    nombre_cientifico = models.CharField(max_length=200)
    cepa = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    
    reino = models.CharField(max_length=100, blank=True, null=True)
    filo = models.CharField(max_length=100, blank=True, null=True)
    clase = models.CharField(max_length=100, blank=True, null=True)
    orden = models.CharField(max_length=100, blank=True, null=True)
    familia = models.CharField(max_length=100, blank=True, null=True)
    
    # Origen y aislamiento
    origen = models.CharField(max_length=200)
    ubicacion_geografica = models.CharField(max_length=300, blank=True, null=True)
    fecha_aislamiento = models.DateField(null=True, blank=True)
    metodo_aislamiento = models.TextField(blank=True, null=True)
    aislado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organismos_aislados')
    
    # Características morfológicas
    color_colonia = models.CharField(max_length=200, blank=True, null=True)
    forma_colonia = models.CharField(max_length=100, blank=True, null=True)
    elevacion = models.CharField(max_length=100, blank=True, null=True)
    borde = models.CharField(max_length=100, blank=True, null=True)
    superficie = models.CharField(max_length=100, blank=True, null=True)
    textura = models.CharField(max_length=100, blank=True, null=True)
    tamano = models.CharField(max_length=50, blank=True, null=True, help_text="En mm")
    tincion_gram = models.CharField(max_length=50, blank=True, null=True)
    observaciones_microscopicas = models.TextField(blank=True, null=True)
    
    # Condiciones de cultivo
    medio_cultivo = models.CharField(max_length=200, blank=True, null=True)
    temperatura_optima = models.CharField(max_length=50, blank=True, null=True)
    ph_optimo = models.CharField(max_length=50, blank=True, null=True)
    tiempo_crecimiento = models.CharField(max_length=100, blank=True, null=True)
    condiciones_oxigeno = models.CharField(max_length=100, blank=True, null=True)
    metodo_conservacion = models.CharField(max_length=200, blank=True, null=True)
    observaciones_cultivo = models.TextField(blank=True, null=True)
    
    # Información adicional
    propiedades_interes = models.TextField(blank=True, null=True)
    aplicaciones_potenciales = models.TextField(blank=True, null=True)
    referencias_bibliograficas = models.TextField(blank=True, null=True)
    notas_generales = models.TextField(blank=True, null=True)
    
    # Metadatos
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organismos_registrados')
    
    class Meta:
        verbose_name = 'Organismo'
        verbose_name_plural = 'Organismos'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['codigo', 'tipo']),
            models.Index(fields=['nombre_cientifico']),
        ]
    
    def __str__(self):
        return f"{self.nombre_cientifico} ({self.codigo})"


class Equipo(models.Model):
    """Equipos del laboratorio"""
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('en_uso', 'En Uso'),
        ('mantenimiento', 'En Mantenimiento'),
        ('fuera_servicio', 'Fuera de Servicio'),
    ]
    
    nombre = models.CharField(max_length=200)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    fabricante = models.CharField(max_length=200, blank=True, null=True)
    
    especificaciones = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=200)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    
    fecha_adquisicion = models.DateField(null=True, blank=True)
    fecha_ultima_calibracion = models.DateField(null=True, blank=True)
    fecha_proxima_calibracion = models.DateField(null=True, blank=True)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True)
    
    procedimientos_uso = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"
    
    def requiere_mantenimiento(self):
        """Verifica si el equipo requiere mantenimiento próximamente"""
        if self.fecha_proximo_mantenimiento:
            dias_restantes = (self.fecha_proximo_mantenimiento - timezone.now().date()).days
            return dias_restantes <= 7
        return False


class MantenimientoEquipo(models.Model):
    """Historial de mantenimientos y calibraciones"""
    TIPOS = [
        ('mantenimiento_preventivo', 'Mantenimiento Preventivo'),
        ('mantenimiento_correctivo', 'Mantenimiento Correctivo'),
        ('calibracion', 'Calibración'),
        ('reparacion', 'Reparación'),
    ]
    
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='mantenimientos')
    tipo = models.CharField(max_length=30, choices=TIPOS)
    fecha = models.DateField()
    descripcion = models.TextField()
    realizado_por = models.CharField(max_length=200)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Mantenimiento de Equipo'
        verbose_name_plural = 'Mantenimientos de Equipos'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.equipo.nombre} ({self.fecha})"


class ArchivoAdjunto(models.Model):
    """Archivos adjuntos a protocolos, organismos o equipos"""
    TIPOS_ENTIDAD = [
        ('protocolo', 'Protocolo'),
        ('organismo', 'Organismo'),
        ('equipo', 'Equipo'),
    ]
    
    CATEGORIAS = [
        ('documento', 'Documento'),
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('dataset', 'Dataset'),
        ('manual', 'Manual'),
        ('certificado', 'Certificado'),
        ('otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(
        upload_to='archivos/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png', 'mp4', 'avi', 'csv'])]
    )
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='documento')
    
    # Relacionar con diferentes entidades
    tipo_entidad = models.CharField(max_length=20, choices=TIPOS_ENTIDAD)
    id_entidad = models.IntegerField()
    
    tamano = models.BigIntegerField(help_text="Tamaño en bytes")
    tipo_archivo = models.CharField(max_length=100)
    
    subido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Archivo Adjunto'
        verbose_name_plural = 'Archivos Adjuntos'
        ordering = ['-fecha_subida']
        indexes = [
            models.Index(fields=['tipo_entidad', 'id_entidad']),
        ]
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_entidad_display()}"
    
    def get_tamano_legible(self):
        """Retorna el tamaño en formato legible"""
        tamano = self.tamano
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if tamano < 1024.0:
                return f"{tamano:.2f} {unidad}"
            tamano /= 1024.0
        return f"{tamano:.2f} TB"


class AuditoriaLog(models.Model):
    """Registro de auditoría inmutable para acciones críticas"""
    ACCIONES = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
        ('validar', 'Validar'),
        ('login', 'Inicio de Sesión'),
        ('logout', 'Cierre de Sesión'),
    ]
    
    ENTIDADES = [
        ('usuario', 'Usuario'),
        ('protocolo', 'Protocolo'),
        ('organismo', 'Organismo'),
        ('equipo', 'Equipo'),
        ('archivo', 'Archivo'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    entidad = models.CharField(max_length=20, choices=ENTIDADES)
    id_entidad = models.IntegerField(null=True, blank=True)
    
    descripcion = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=300, blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    datos_adicionales = models.JSONField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['usuario', 'timestamp']),
            models.Index(fields=['entidad', 'id_entidad']),
        ]
    
    def __str__(self):
        return f"{self.get_accion_display()} - {self.get_entidad_display()} por {self.usuario} ({self.timestamp})"


class Notificacion(models.Model):
    """Notificaciones para usuarios"""
    TIPOS = [
        ('info', 'Información'),
        ('advertencia', 'Advertencia'),
        ('error', 'Error'),
        ('exito', 'Éxito'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='info')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    
    # Enlace opcional a una entidad
    entidad_tipo = models.CharField(max_length=20, blank=True, null=True)
    entidad_id = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    def marcar_como_leida(self):
        """Marca la notificación como leída"""
        if not self.leida:
            self.leida = True
            self.fecha_lectura = timezone.now()
            self.save()