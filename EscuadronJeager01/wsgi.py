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

admin_username = 'ADMINJAAL'
admin_email = 'joseabacu0001@gmail.com'
admin_password = 'L1JAAL08'  # Puedes cambiar esto por una contraseña segura

try:
    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        print("✅ Superusuario creado correctamente.")
    else:
        print("⚠️ El superusuario ya existe. No se creó uno nuevo.")
except Exception as e:
    print(f"❌ Error al crear el superusuario: {e}")

# Activar la aplicación
application = get_wsgi_application()
