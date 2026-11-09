from django.contrib import admin

from .models import CategoriaCurso, Curso

admin.site.site_header = 'CodeAcademy Hub - Panel de Control'
admin.site.site_title = 'CodeAcademy Hub Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'


@admin.register(CategoriaCurso)
class CategoriaCursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'precio', 'cupos', 'estado', 'vigente')
    list_filter = ('categoria', 'estado', 'vigente')
    search_fields = ('codigo', 'nombre', 'descripcion')
    list_editable = ('cupos', 'estado', 'vigente')
    list_select_related = ('categoria',)
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'nombre', 'categoria'),
        }),
        ('Contenido', {
            'fields': ('descripcion', 'imagen'),
        }),
        ('Condiciones comerciales', {
            'fields': ('precio', 'cupos', 'estado'),
        }),
        ('Control de vigencia', {
            'fields': ('vigente', 'fecha_creacion'),
        }),
    )