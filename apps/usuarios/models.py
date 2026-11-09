from django.conf import settings
from django.db import models

from .validators import validar_rut


class Perfil(models.Model):
    class Rol(models.TextChoices):
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        ADMINISTRATIVO = 'ADMINISTRATIVO', 'Administrativo'

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(max_length=15, choices=Rol.choices, default=Rol.ESTUDIANTE)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'{self.usuario.username} ({self.get_rol_display()})'

    def save(self, *args, **kwargs):
        self.rut = validar_rut(self.rut)
        super().save(*args, **kwargs)