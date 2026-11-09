from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistroForm
from .models import Perfil


def registro(request):
    if request.user.is_authenticated:
        return redirect('cursos:lista')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'¡Bienvenido/a, {usuario.first_name}! Tu cuenta fue creada.')
            return redirect('cursos:lista')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil_ver(request):
    perfil = Perfil.objects.filter(usuario=request.user).first()
    return render(request, 'usuarios/perfil.html', {'perfil': perfil})