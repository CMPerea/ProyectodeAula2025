from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('lista_organismos/', views.listar_organismos_view, name = 'lista'),
    
    #path('homepage/', views.listaProtocolos, name='homepage'),
    #path('protocolo/', views.protocolo_view, name='protocolo')

]
