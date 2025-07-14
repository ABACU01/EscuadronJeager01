from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# PERFIL Y RANGOS
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    RANGOS = [
        ('soldado', 'Soldado'),
        ('capitan', 'Capitán'),
        ('general', 'General'),
    ]
    rango = models.CharField(max_length=10, choices=RANGOS, default='soldado')

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rango_display()})"

# GUERRA Y ALIANZA ENEMIGA
class Guerra(models.Model):
    nombre = models.CharField(max_length=100)
    alianza_enemiga = models.CharField(max_length=100)
    en_curso = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} vs {self.alianza_enemiga}"

# MIEMBROS DE LA ALIANZA ENEMIGA
class MiembroAlianza(models.Model):
    guerra = models.ForeignKey(Guerra, on_delete=models.CASCADE, related_name='miembros')
    nombre_jugador = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_jugador} (Guerra: {self.guerra.nombre})"

# ENEMIGOS REGISTRADOS
from django.utils import timezone
from datetime import timedelta

class Enemigo(models.Model):
    guerra = models.ForeignKey(Guerra, on_delete=models.CASCADE, related_name='enemigos')
    nombre = models.CharField(max_length=100)
    coordenadas = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    ultima_vez_atacado = models.DateTimeField(null=True, blank=True)

    def ha_regenerado(self):
        if not self.ultima_vez_atacado:
            return True
        tiempo = timezone.now() - self.ultima_vez_atacado
        return tiempo.total_seconds() >= 3 * 3600  # 3 horas

    def tiempo_restante(self):
        # Duración total para regenerar en segundos (3 horas)
        duracion_regeneracion = 3 * 3600

        if not self.ultima_vez_atacado:
            return 0  # Ya regenerado, no queda tiempo

        tiempo_transcurrido = (timezone.now() - self.ultima_vez_atacado).total_seconds()
        tiempo_faltante = duracion_regeneracion - tiempo_transcurrido

        if tiempo_faltante < 0:
            return 0  # Ya terminó la regeneración

        return int(tiempo_faltante)  # Devuelve segundos restantes como entero

    def __str__(self):
        return f"{self.nombre} [{self.coordenadas}]"


# MEJORAS DE EDIFICIOS
from django.core.exceptions import ValidationError

class MejoraEdificio(models.Model):
    CATEGORIAS = [
        ('recursos', 'Recursos'),
        ('ejercito', 'Ejército'),
        ('torretas', 'Torretas'),
        ('defensas', 'Defensas'),
        ('base_estelar', 'Base Estelar'),
    ]

    EDIFICIOS = {
        'recursos': [
            ('casas_compactas', 'Casas Compactas'),
            ('minas', 'Minas'),
            ('bancos', 'Bancos'),
            ('silos', 'Silos'),
            ('observatorio', 'Observatorio'),
            ('refineria', 'Refinería'),
        ],
        'ejercito': [
            ('portal_estelar', 'Portal Estelar'),
            ('campo_entrenamiento', 'Campo de Entrenamiento'),
            ('fabrica', 'Fábrica'),
            ('puerto_estelar', 'Puerto Estelar'),
            ('laboratorio', 'Laboratorio'),
            ('embajada', 'Embajada'),
        ],
        'torretas': [
            ('canon', 'Cañón'),
            ('torre_tiro', 'Torre de Tiro'),
            ('torre_laser', 'Torre Láser'),
            ('lanzamisiles', 'Lanzamisiles'),
            ('torre_gelida', 'Torre Gélida'),
            ('mortero', 'Mortero'),
        ],
        'defensas': [
            ('bunker_amigos', 'Búnker de Amigos'),
            ('bunker_defensas', 'Búnker de Defensas'),
        ],
        'base_estelar': [
            ('base_estelar', 'Base Estelar'),
        ],
    }

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    edificio = models.CharField(max_length=30)  # Validaremos manualmente según la categoria
    
    nivel_inicial = models.IntegerField()
    nivel_objetivo = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    duracion_horas = models.IntegerField()

    planeta_principal = models.BooleanField(default=True)
    numero_colonia = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        # Validar que el edificio esté dentro de la categoría elegida
        edificios_validos = dict(self.EDIFICIOS).get(self.categoria, [])
        # edificios_validos es una lista de tuplas, obtener solo las keys
        edificios_validos_keys = [ed[0] for ed in self.EDIFICIOS.get(self.categoria, [])]
        if self.edificio not in edificios_validos_keys:
            raise ValidationError(f"Edificio inválido para la categoría {self.categoria}")

        # Si no es planeta principal, número de colonia es obligatorio
        if not self.planeta_principal and not self.numero_colonia:
            raise ValidationError("Debe especificar el número de colonia si no es el planeta principal.")

        # Si es planeta principal, número de colonia debe ser None
        if self.planeta_principal and self.numero_colonia is not None:
            raise ValidationError("El planeta principal no debe tener número de colonia.")

    def tiempo_restante(self):
        from datetime import timedelta
        from django.utils import timezone
        fin = self.fecha_inicio + timedelta(hours=self.duracion_horas)
        return max(fin - timezone.now(), timedelta(seconds=0))

    def __str__(self):
        return f"{self.usuario.username}: {self.get_categoria_display()} - {self.get_edificio_display()} " \
            f"Nivel {self.nivel_inicial} → {self.nivel_objetivo}"

    def get_edificio_display(self):
        # Buscar el nombre legible según categoría y código edificio
        for key, lista in self.EDIFICIOS.items():
            for codigo, nombre in lista:
                if codigo == self.edificio:
                    return nombre
        return self.edificio

class MiembroAlianzaPropia(models.Model):
    guerra = models.ForeignKey(Guerra, on_delete=models.CASCADE, related_name='miembros_propios')
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    alias_juego = models.CharField(max_length=100, default='Desconocido')  # ✔️ Ya no preguntará
    nivel = models.IntegerField(default=0)  # ✔️ Por ejemplo, nivel 0
    estrellas = models.IntegerField(default=0)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.perfil.usuario.username} - {self.perfil.get_rango_display()} (Guerra: {self.guerra.nombre})"
