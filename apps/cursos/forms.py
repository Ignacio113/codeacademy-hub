from django import forms

from .models import Curso


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
            'codigo', 'nombre', 'categoria', 'descripcion',
            'precio', 'cupos', 'estado', 'imagen', 'vigente',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. PY-101'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'vigente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip().upper()
        repetido = Curso.objects.filter(codigo__iexact=codigo).exclude(pk=self.instance.pk)
        if repetido.exists():
            raise forms.ValidationError('Ya existe un curso con ese código.')
        return codigo

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_cupos(self):
        cupos = self.cleaned_data['cupos']
        if cupos < 0:
            raise forms.ValidationError('Los cupos no pueden ser negativos.')
        return cupos