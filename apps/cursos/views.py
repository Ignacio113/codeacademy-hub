from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import CategoriaCurso, Curso


def curso_lista(request):
    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    orden = request.GET.get('orden', 'nombre')

    cursos = Curso.objects.filter(vigente=True).select_related('categoria')

    if busqueda:
        cursos = cursos.filter(
            Q(nombre__icontains=busqueda)
            | Q(codigo__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
        )

    if categoria_id.isdigit():
        cursos = cursos.filter(categoria_id=categoria_id)

    ordenes = {
        'nombre': 'nombre',
        'precio_asc': 'precio',
        'precio_desc': '-precio',
        'recientes': '-fecha_creacion',
    }
    cursos = cursos.order_by(ordenes.get(orden, 'nombre'))

    paginador = Paginator(cursos, 6)
    pagina = paginador.get_page(request.GET.get('page'))

    parametros = request.GET.copy()
    parametros.pop('page', None)

    return render(request, 'cursos/curso_lista.html', {
        'pagina': pagina,
        'categorias': CategoriaCurso.objects.all(),
        'busqueda': busqueda,
        'categoria_id': categoria_id,
        'orden': orden,
        'parametros': parametros.urlencode(),
    })


def curso_detalle(request, codigo):
    curso = get_object_or_404(
        Curso.objects.select_related('categoria'),
        codigo=codigo,
        vigente=True,
    )
    return render(request, 'cursos/curso_detalle.html', {'curso': curso})