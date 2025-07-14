from django import forms
from app_guerra.models import MejoraEdificio

class MejoraForm(forms.ModelForm):
    class Meta:
        model = MejoraEdificio
        fields = [
            'categoria',
            'edificio',
            'nivel_inicial',
            'nivel_objetivo',
            'fecha_inicio',
            'duracion_horas',
            'planeta_principal',
            'numero_colonia',
        ]
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'numero_colonia': forms.NumberInput(attrs={'placeholder': 'Si aplica'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Preparar las opciones con data-categoria (para usar en el template si se quiere)
        self.edificio_opciones = []
        for categoria, edificios in MejoraEdificio.EDIFICIOS.items():
            for value, label in edificios:
                self.edificio_opciones.append({
                    'value': value,
                    'label': label,
                    'categoria': categoria,
                })

        # Establecer todas las opciones por defecto (opcional)
        self.fields['edificio'].choices = [
            (ed['value'], ed['label']) for ed in self.edificio_opciones
        ]






from django import forms
from .models import Enemigo

class EnemigoForm(forms.ModelForm):
    class Meta:
        model = Enemigo
        fields = ['guerra', 'nombre', 'coordenadas', 'observaciones', 'ultima_vez_atacado']
        widgets = {
            'guerra': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'coordenadas': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ultima_vez_atacado': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        labels = {
            'guerra': 'Guerra',
            'nombre': 'Nombre del enemigo',
            'coordenadas': 'Coordenadas',
            'observaciones': 'Observaciones (opcional)',
            'ultima_vez_atacado': 'Última vez atacado (opcional)',
        }
