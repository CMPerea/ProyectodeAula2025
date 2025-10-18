from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.homepage_view, name='homepage'),
    path('protocolo/', views.protocolo_view, name='protocolo'),
]
