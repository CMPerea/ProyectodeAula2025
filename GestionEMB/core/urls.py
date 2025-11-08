from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('lista_organismos/', views.listar_organismos_view, name = 'lista'),
    path('crear_organismo/', views.crear_organismo_view, name='crear_organismo'),
    path('protocolos/', views.listaProtocolos, name='listaProcolos'),
    path('protocolo/', views.protocolo_view, name='protocolo'),
    path('protocolo/<int:protocolo_id>/', views.protocolo_detalle_view, name='protocolo_detalle'),
    path('protocolo/editar/<int:protocolo_id>/', views.protocolo_editar_view, name='protocolo_editar'),
    path('protocolo/eliminar/<int:protocolo_id>/', views.protocolo_eliminar_view, name='protocolo_eliminar'),
    path('protocolo/<int:protocolo_id>/archivo/eliminar/<int:archivo_id>/', views.protocolo_archivo_eliminar_view, name='protocolo_archivo_eliminar'),
    path('usuarios/registrar/', views.registrar_usuario_view, name='registrar_usuario'),
    
    #path('homepage/', views.listaProtocolos, name='homepage'),
    #path('protocolo/', views.protocolo_view, name='protocolo')

]
