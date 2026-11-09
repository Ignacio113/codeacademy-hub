from django.urls import path

from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.curso_lista, name='lista'),
    path('curso/<str:codigo>/', views.curso_detalle, name='detalle'),
]