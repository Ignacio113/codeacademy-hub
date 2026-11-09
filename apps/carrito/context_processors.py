from .carrito import obtener_carrito


def carrito_contador(request):
    return {'carrito_cantidad': len(obtener_carrito(request))}