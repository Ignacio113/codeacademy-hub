from apps.cursos.models import Curso

CLAVE_SESION = 'carrito'
DESCUENTO_MINIMO_CURSOS = 3
DESCUENTO_PORCENTAJE = 10


def obtener_carrito(request):
    return request.session.get(CLAVE_SESION, {})


def guardar_carrito(request, carrito):
    request.session[CLAVE_SESION] = carrito


def calcular_resumen(request):
    carrito = obtener_carrito(request)
    cursos = (
        Curso.objects.select_related('categoria')
        .filter(codigo__in=list(carrito), vigente=True)
        .order_by('nombre')
    )

    items = []
    subtotal = 0
    for curso in cursos:
        cantidad = carrito[curso.codigo]
        subtotal_item = curso.precio * cantidad
        subtotal += subtotal_item
        items.append({
            'curso': curso,
            'cantidad': cantidad,
            'subtotal': subtotal_item,
        })

    aplica_descuento = len(items) >= DESCUENTO_MINIMO_CURSOS
    descuento = subtotal * DESCUENTO_PORCENTAJE // 100 if aplica_descuento else 0

    return {
        'items': items,
        'subtotal': subtotal,
        'descuento': descuento,
        'total': subtotal - descuento,
        'aplica_descuento': aplica_descuento,
        'porcentaje': DESCUENTO_PORCENTAJE,
        'faltan': max(0, DESCUENTO_MINIMO_CURSOS - len(items)),
    }