# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=9)
    activo = models.IntegerField()
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria'


class Configuracion(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    clave = models.CharField(unique=True, max_length=100)
    valor = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_dato = models.CharField(max_length=7)
    categoria = models.CharField(max_length=50)
    modificable_usuario = models.IntegerField()
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configuracion'


class Equipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(unique=True, max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    especificaciones_tecnicas = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=17)
    fecha_adquision = models.DateField(blank=True, null=True)
    fecha_ultimo_mantenimiento = models.DateField(blank=True, null=True)
    fecha_proximo_mantenimiento = models.DateField(blank=True, null=True)
    responsable = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, blank=True, null=True)
    activo = models.IntegerField()
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipo'


class HistorialMantenimiento(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    equipo = models.ForeignKey(Equipo, models.DO_NOTHING)
    tipo_mantenimiento = models.CharField(max_length=11)
    fecha_mantenimiento = models.DateField()
    descripcion = models.TextField()
    realizado_por = models.CharField(max_length=255, blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    proximo_mantenimiento = models.DateField(blank=True, null=True)
    registrado_por = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='registrado_por')
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_mantenimiento'
# Unable to inspect table 'notificacion'
# The error was: (1146, "Table 'emb_protocolos.notificacion' doesn't exist")


class Organismo(models.Model):
    id_organismo = models.AutoField(primary_key=True)
    nombre_cientifico = models.CharField(max_length=255)
    cepa = models.CharField(max_length=100, blank=True, null=True)
    codigo_identificacion = models.CharField(unique=True, max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=19)
    origen = models.CharField(max_length=255, blank=True, null=True)
    caracteristicas_morfologicas = models.TextField(blank=True, null=True)
    condiciones_cultivo = models.TextField(blank=True, null=True)
    temperatura_optima = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    ph_optimo = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    creador = models.ForeignKey('Usuario', models.DO_NOTHING)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organismo'
        unique_together = (('nombre_cientifico', 'cepa'),)


class Protocolo(models.Model):
    id_protocolo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    procedimiento = models.TextField()
    materiales = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=11)
    autor = models.ForeignKey('Usuario', models.DO_NOTHING)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)
    fecha_validacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protocolo'


class ProtocoloEquipo(models.Model):
    id_protocolo_equipo = models.AutoField(primary_key=True)
    protocolo = models.ForeignKey(Protocolo, models.DO_NOTHING)
    equipo = models.ForeignKey(Equipo, models.DO_NOTHING)
    notas = models.TextField(blank=True, null=True)
    fecha_asociacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protocolo_equipo'
        unique_together = (('protocolo', 'equipo'),)


class ProtocoloOrganismo(models.Model):
    id_protocolo_organismo = models.AutoField(primary_key=True)
    protocolo = models.ForeignKey(Protocolo, models.DO_NOTHING)
    organismo = models.ForeignKey(Organismo, models.DO_NOTHING)
    tipo_relacion = models.CharField(max_length=10)
    notas = models.TextField(blank=True, null=True)
    fecha_asociacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protocolo_organismo'
        unique_together = (('organismo', 'protocolo'),)


class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    rol = models.CharField(max_length=13)
    activo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'usuario'
