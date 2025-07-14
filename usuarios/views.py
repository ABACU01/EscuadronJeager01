from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render

def inicio(request):
    return render(request, 'usuarios/registro.html')  # o 'usuarios/inicio.html' si es otro archivo



from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from app_guerra.models import Perfil


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST.get('password2')  # opcional si lo usas

        # Validación: contraseñas iguales
        if password != password2:
            messages.error(request, '❌ Las contraseñas no coinciden.')
            return render(request, 'usuarios/registro.html')

        # Validación: usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ El nombre de usuario ya está en uso.')
            return render(request, 'usuarios/registro.html')

        # Validación: email ya registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ El correo ya está registrado.')
            return render(request, 'usuarios/registro.html')

        # Crear usuario inactivo
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Cuenta inactiva hasta que el admin la apruebe
        user.save()

        return render(request, 'usuarios/pendiente.html')  # Página de espera

    return render(request, 'usuarios/registro.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('perfil')  # Cambia 'perfil' a la vista a la que quieres redirigir
            else:
                messages.error(request, 'Tu cuenta está pendiente de aprobación.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user
    })




def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
