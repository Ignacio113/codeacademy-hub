from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Perfil
from .validators import validar_rut


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = 'form-control'


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(label='Nombres', max_length=150)
    last_name = forms.CharField(label='Apellidos', max_length=150)
    email = forms.EmailField(label='Correo electrónico')
    rut = forms.CharField(label='RUT', max_length=12, help_text='Ejemplo: 12345678-5')
    telefono = forms.CharField(label='Teléfono', max_length=15, required=False)

    field_order = [
        'username', 'first_name', 'last_name', 'email',
        'rut', 'telefono', 'password1', 'password2',
    ]

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con ese correo.')
        return email

    def clean_rut(self):
        rut = validar_rut(self.cleaned_data['rut'])
        if Perfil.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Ya existe una cuenta con ese RUT.')
        return rut

    @transaction.atomic
    def save(self, commit=True):
        usuario = super().save(commit)
        Perfil.objects.create(
            usuario=usuario,
            rut=self.cleaned_data['rut'],
            telefono=self.cleaned_data['telefono'],
            rol=Perfil.Rol.ESTUDIANTE,
        )
        return usuario