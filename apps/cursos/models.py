from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class CategoriaCurso(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        AGOTADO = 'AGOTADO', 'Agotado'
        SUSPENDIDO = 'SUSPENDIDO', 'Suspendido'
        PROXIMAMENTE = 'PROXIMAMENTE', 'Próximamente'

    categoria = models.ForeignKey(
        CategoriaCurso,
        on_delete=models.PROTECT,
        related_name='cursos',
    )
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.IntegerField(validators=[MinValueValidator(0)])
    cupos = models.IntegerField(validators=[MinValueValidator(0)])
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.DISPONIBLE,
    )
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True)
    vigente = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'