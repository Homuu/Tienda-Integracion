from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pago/', views.pago, name='pago'),
    path('retorno/', views.retorno, name='retorno'),
    path('rechazo/', views.rechazo, name='rechazo'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]