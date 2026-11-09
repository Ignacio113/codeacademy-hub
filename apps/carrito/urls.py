from django.urls import path

from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.carrito_ver, name='ver'),
    path('agregar/<str:codigo>/', views.carrito_agregar, name='agregar'),
    path('actualizar/<str:codigo>/', views.carrito_actualizar, name='actualizar'),
    path('quitar/<str:codigo>/', views.carrito_quitar, name='quitar'),
    path('vaciar/', views.carrito_vaciar, name='vaciar'),
    path('confirmar/', views.carrito_confirmar, name='confirmar'),
]