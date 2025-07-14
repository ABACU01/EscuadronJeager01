from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Creamos una clase personalizada para mostrar el campo is_active
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')  # lo que se ve en la tabla
    list_filter = ('is_active', 'is_staff')  # filtros laterales
    search_fields = ('username', 'email')  # búsqueda
    ordering = ('username',)

# Primero desregistramos al admin original del modelo User
admin.site.unregister(User)

# Registramos el nuevo admin personalizado
admin.site.register(User, CustomUserAdmin)
