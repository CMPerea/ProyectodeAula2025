from django import forms
from .models import Protocolo

class ProtocoloForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        fields = ['titulo',
            'descripcion',
            'procedimiento',
            'materiales',
            'estado',
            'autor',
            'categoria',
            'fecha_validacion',]
        