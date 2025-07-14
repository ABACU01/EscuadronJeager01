"""
WSGI config for EscuadronJeager01 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EscuadronJeager01.settings')

# Configuramos Django
django.setup()

# Ejecutamos las migraciones automáticamente al iniciar la app
try:
    call_command('migrate', interactive=False)
except Exception as e:
    # Aquí puedes poner un print para ver errores, o manejar el error de otra forma
    print(f"Error al correr migraciones automáticamente: {e}")

application = get_wsgi_application()
