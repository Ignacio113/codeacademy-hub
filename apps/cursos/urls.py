from django.urls import path

from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.curso_lista, name='lista'),
    path('curso/<str:codigo>/', views.curso_detalle, name='detalle'),
    path('gestion/', views.curso_gestion, name='gestion'),
    path('gestion/nuevo/', views.curso_crear, name='crear'),
    path('gestion/<str:codigo>/editar/', views.curso_editar, name='editar'),
    path('gestion/<str:codigo>/eliminar/', views.curso_eliminar, name='eliminar'),
]