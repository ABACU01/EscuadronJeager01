"""
WSGI config for EscuadronJeager01 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EscuadronJeager01.settings')

# Iniciar Django
django.setup()

# 🔧 Hacer migraciones
from django.core.management import call_command
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Error al aplicar migraciones: {e}")

# 👤 Crear superusuario si no existe
from django.contrib.auth import get_user_model
User = get_user_model()

admin_username = 'admin'
admin_email = 'admin@correo.com'
admin_password = 'admin1234'

try:
    user = User.objects.filter(username=admin_username).first()
    if user:
        if not user.is_superuser:
            user.is_superuser = True
            user.is_staff = True
            user.set_password(admin_password)
            user.save()
            print("🔄 Usuario existente actualizado a superusuario.")
        else:
            print("✅ El superusuario ya existe.")
    else:
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        print("✅ Superusuario creado correctamente.")
except Exception as e:
    print(f"❌ Error al verificar/crear superusuario: {e}")
