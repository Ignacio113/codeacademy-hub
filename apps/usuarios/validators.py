from django.core.exceptions import ValidationError


def validar_rut(valor):
    limpio = valor.replace('.', '').replace('-', '').replace(' ', '').upper()
    if len(limpio) < 2 or not limpio[:-1].isdigit():
        raise ValidationError('Ingresa un RUT válido, por ejemplo 12345678-5.')

    cuerpo, digito = limpio[:-1], limpio[-1]

    suma = 0
    factor = 2
    for numero in reversed(cuerpo):
        suma += int(numero) * factor
        factor = 2 if factor == 7 else factor + 1

    resto = 11 - suma % 11
    esperado = '0' if resto == 11 else 'K' if resto == 10 else str(resto)
    if digito != esperado:
        raise ValidationError('El RUT no es válido (dígito verificador incorrecto).')

    return f'{int(cuerpo)}-{digito}'