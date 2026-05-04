from django import forms
from datetime import date
from .models import Reserva

FIELD_CLASS = 'form-control'
SELECT_CLASS = 'form-select'


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['habitacion', 'fecha_entrada', 'fecha_salida', 'num_huespedes']
        widgets = {
            'habitacion': forms.Select(attrs={'class': SELECT_CLASS}),
            'fecha_entrada': forms.DateInput(
                attrs={'type': 'date', 'class': FIELD_CLASS, 'min': date.today().isoformat()}
            ),
            'fecha_salida': forms.DateInput(
                attrs={'type': 'date', 'class': FIELD_CLASS, 'min': date.today().isoformat()}
            ),
            'num_huespedes': forms.NumberInput(attrs={'class': FIELD_CLASS, 'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')
        habitacion = cleaned_data.get('habitacion')
        num_huespedes = cleaned_data.get('num_huespedes')

        if fecha_entrada and fecha_salida:
            if fecha_entrada >= fecha_salida:
                raise forms.ValidationError('La fecha de salida debe ser posterior a la fecha de entrada.')
            if fecha_entrada < date.today():
                raise forms.ValidationError('La fecha de entrada no puede ser en el pasado.')

            if habitacion:
                reservas_conflicto = Reserva.objects.filter(
                    habitacion=habitacion,
                    estado__in=['pendiente', 'confirmada'],
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada,
                )
                if reservas_conflicto.exists():
                    raise forms.ValidationError('La habitación no está disponible en las fechas seleccionadas.')

        if habitacion and num_huespedes and num_huespedes > habitacion.capacidad:
            raise forms.ValidationError(
                f'Esta habitación tiene capacidad máxima de {habitacion.capacidad} personas.'
            )
        return cleaned_data
