from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, ActualizarPerfilForm


def vista_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        if user:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.first_name or user.email}!')
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    return render(request, 'accounts/login.html')


def vista_logout(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('home')


def vista_registro(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistroForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, '¡Cuenta creada exitosamente! Bienvenido al Hotel Pacific Reef.')
        return redirect('home')
    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def vista_perfil(request):
    perfil = getattr(request.user, 'perfil', None)
    if request.method == 'POST':
        form = ActualizarPerfilForm(request.POST, instance=perfil, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form = ActualizarPerfilForm(instance=perfil, user=request.user)
    return render(request, 'accounts/perfil.html', {'usuario': request.user, 'form': form, 'perfil': perfil})
# Épica 1: Gestión de Acceso y Perfiles — HU-01, HU-02, RF-01, RF-02
