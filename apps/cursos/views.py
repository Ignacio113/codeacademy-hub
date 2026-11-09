from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import CursoForm
from .models import CategoriaCurso, Curso


def es_personal(usuario):
    return usuario.is_staff


personal_requerido = user_passes_test(
    es_personal,
    login_url='cursos:lista',
    redirect_field_name=None,
)

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


@login_required
@personal_requerido
def curso_gestion(request):
    cursos = Curso.objects.select_related('categoria').order_by('codigo')
    return render(request, 'cursos/curso_gestion.html', {'cursos': cursos})

@login_required
@personal_requerido
def curso_crear(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save()
            messages.success(request, f'Curso "{curso.nombre}" creado correctamente.')
            return redirect('cursos:gestion')
    else:
        form = CursoForm()
    return render(request, 'cursos/curso_form.html', {
        'form': form,
        'titulo': 'Nuevo curso',
    })

@login_required
@personal_requerido
def curso_editar(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curso "{curso.nombre}" actualizado correctamente.')
            return redirect('cursos:gestion')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/curso_form.html', {
        'form': form,
        'curso': curso,
        'titulo': f'Editar curso {curso.codigo}',
    })

@login_required
@personal_requerido
def curso_eliminar(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    if request.method == 'POST':
        curso.vigente = False
        curso.save(update_fields=['vigente'])
        messages.warning(request, f'Curso "{curso.nombre}" dado de baja. Ya no aparece en el catálogo.')
        return redirect('cursos:gestion')
    return render(request, 'cursos/curso_confirmar_baja.html', {'curso': curso})