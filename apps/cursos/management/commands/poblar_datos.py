from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.cursos.models import CategoriaCurso, Curso


class Command(BaseCommand):
    help = 'Carga categorías, cursos y usuarios de prueba en la base de datos'

    def handle(self, *args, **options):
        # 1. Categorías
        nombres_categorias = {
            'Programación': 'Lenguajes, frameworks y desarrollo de software.',
            'Redes': 'Configuración, administración y diseño de redes.',
            'Ciberseguridad': 'Protección de sistemas, redes y datos.',
            'Bases de Datos': 'Modelado, consultas y administración de datos.',
        }
        categorias = {}
        for nombre, descripcion in nombres_categorias.items():
            categoria, _ = CategoriaCurso.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion},
            )
            categorias[nombre] = categoria

        # 2. Cursos
        cursos = [
            ('PY-101', 'Python desde Cero', 'Programación', 49990, 30,
             'DISPONIBLE', True,
             'Fundamentos de Python: variables, funciones y estructuras de control.'),
            ('DJ-201', 'Desarrollo Web con Django', 'Programación', 79990, 20,
             'DISPONIBLE', True,
             'Construye aplicaciones web completas con el framework Django.'),
            ('JS-102', 'JavaScript Moderno', 'Programación', 59990, 0,
             'AGOTADO', True,
             'ES6+, DOM y programación asíncrona para la web.'),
            ('RD-101', 'Fundamentos de Redes', 'Redes', 54990, 25,
             'DISPONIBLE', True,
             'Modelo OSI, direccionamiento IP y configuración básica de redes.'),
            ('RD-201', 'Administración de Redes Cisco', 'Redes', 89990, 15,
             'PROXIMAMENTE', True,
             'Routing y switching con Cisco Packet Tracer.'),
            ('CS-101', 'Introducción a la Ciberseguridad', 'Ciberseguridad', 64990, 40,
             'DISPONIBLE', True,
             'Amenazas, vulnerabilidades y buenas prácticas de seguridad.'),
            ('CS-301', 'Hacking Ético', 'Ciberseguridad', 99990, 12,
             'SUSPENDIDO', False,
             'Pruebas de penetración con herramientas profesionales.'),
            ('BD-101', 'SQL y Modelado de Datos', 'Bases de Datos', 52990, 35,
             'DISPONIBLE', True,
             'Diseño relacional, consultas SQL y normalización.'),
        ]
        for codigo, nombre, cat, precio, cupos, estado, vigente, desc in cursos:
            Curso.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'categoria': categorias[cat],
                    'precio': precio,
                    'cupos': cupos,
                    'estado': estado,
                    'vigente': vigente,
                    'descripcion': desc,
                },
            )

        # 3. Usuarios de prueba
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@codeacademyhub.cl',
                password='Admin12345',
            )
        if not User.objects.filter(username='estudiante').exists():
            User.objects.create_user(
                username='estudiante',
                email='estudiante@codeacademyhub.cl',
                password='Estudiante12345',
            )

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados correctamente.'))