from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from apps.cursos.models import Curso

from .carrito import (
    CLAVE_SESION,
    calcular_resumen,
    guardar_carrito,
    obtener_carrito,
)


def carrito_ver(request):
    return render(request, 'carrito/carrito.html', calcular_resumen(request))


@require_POST
def carrito_agregar(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo, vigente=True)

    if curso.estado != Curso.Estado.DISPONIBLE or curso.cupos < 1:
        messages.error(request, f'El curso "{curso.nombre}" no tiene cupos disponibles.')
        return redirect('cursos:detalle', codigo=codigo)

    carrito = obtener_carrito(request)
    actual = carrito.get(codigo, 0)

    if actual + 1 > curso.cupos:
        messages.warning(request, f'Solo quedan {curso.cupos} cupos en "{curso.nombre}".')
        return redirect('carrito:ver')

    carrito[codigo] = actual + 1
    guardar_carrito(request, carrito)
    messages.success(request, f'"{curso.nombre}" agregado al carrito.')
    return redirect('carrito:ver')


@require_POST
def carrito_actualizar(request, codigo):
    carrito = obtener_carrito(request)
    if codigo not in carrito:
        return redirect('carrito:ver')

    curso = get_object_or_404(Curso, codigo=codigo, vigente=True)

    try:
        cantidad = int(request.POST.get('cantidad', ''))
    except ValueError:
        messages.error(request, 'La cantidad ingresada no es válida.')
        return redirect('carrito:ver')

    if cantidad < 1:
        messages.error(request, 'La cantidad mínima es 1. Usa "Quitar" para sacar el curso.')
    elif cantidad > curso.cupos:
        messages.warning(request, f'Solo quedan {curso.cupos} cupos en "{curso.nombre}".')
    else:
        carrito[codigo] = cantidad
        guardar_carrito(request, carrito)
        messages.success(request, f'Cupos de "{curso.nombre}" actualizados a {cantidad}.')
    return redirect('carrito:ver')


@require_POST
def carrito_quitar(request, codigo):
    carrito = obtener_carrito(request)
    if carrito.pop(codigo, None) is not None:
        guardar_carrito(request, carrito)
        messages.info(request, 'Curso quitado del carrito.')
    return redirect('carrito:ver')


@require_POST
def carrito_vaciar(request):
    request.session.pop(CLAVE_SESION, None)
    messages.info(request, 'Carrito vaciado.')
    return redirect('carrito:ver')

@login_required
@require_POST
def carrito_confirmar(request):
    resumen = calcular_resumen(request)
    if not resumen['items']:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('cursos:lista')

    ahora = timezone.localtime()
    resumen['fecha'] = ahora
    resumen['codigo_solicitud'] = f'SOL-{ahora:%Y%m%d%H%M%S}'

    request.session.pop(CLAVE_SESION, None)
    return render(request, 'carrito/comprobante.html', resumen)