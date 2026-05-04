import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario

FIELD_CLASS = 'form-control'
SELECT_CLASS = 'form-select'

TIPO_DOC_CHOICES = [
    ('run', 'RUN'),
    ('pasaporte', 'Pasaporte'),
]


def _unique_username(email):
    base = re.sub(r'[^\w]', '', email.split('@')[0])[:25] or 'usuario'
    username = base
    n = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{n}"
        n += 1
    return username


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, label='Nombre',
        widget=forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Tu nombre'}))
    last_name = forms.CharField(
        max_length=50, label='Apellido',
        widget=forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Tu apellido'}))
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': FIELD_CLASS, 'placeholder': 'correo@ejemplo.com'}))
    telefono = forms.CharField(
        max_length=20, required=False, label='Teléfono',
        widget=forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': '+56 9 1234 5678'}))
    tipo_documento = forms.ChoiceField(
        choices=TIPO_DOC_CHOICES, label='Tipo de documento',
        widget=forms.Select(attrs={'class': SELECT_CLASS}))
    numero_documento = forms.CharField(
        max_length=20, required=True, label='Número de documento',
        widget=forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': '12.345.678-9'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields['password1'].widget.attrs.update({'class': FIELD_CLASS})
        self.fields['password2'].widget.attrs.update({'class': FIELD_CLASS})
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta registrada con este correo electrónico.')
        return email

    def clean_numero_documento(self):
        tipo = self.cleaned_data.get('tipo_documento')
        numero = self.cleaned_data.get('numero_documento', '').strip().upper()
        if tipo == 'run':
            if not re.match(r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dKk]$', numero):
                raise forms.ValidationError(
                    'Ingrese un RUN válido (ej: 12.345.678-9 o 12345678-9).')
        elif tipo == 'pasaporte':
            if len(numero) < 6:
                raise forms.ValidationError('Ingrese un número de pasaporte válido.')
        return numero

    def save(self, commit=True):
        email = self.cleaned_data['email'].lower()
        user = User(
            username=_unique_username(email),
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=email,
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                usuario=user,
                telefono=self.cleaned_data.get('telefono', ''),
                tipo_documento=self.cleaned_data.get('tipo_documento', 'run'),
                rut=self.cleaned_data.get('numero_documento', ''),
            )
        return user


class ActualizarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50, label='Nombre',
        widget=forms.TextInput(attrs={'class': FIELD_CLASS}))
    last_name = forms.CharField(
        max_length=50, label='Apellido',
        widget=forms.TextInput(attrs={'class': FIELD_CLASS}))
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': FIELD_CLASS}))

    class Meta:
        model = PerfilUsuario
        fields = ['tipo_documento', 'rut', 'telefono']
        labels = {
            'tipo_documento': 'Tipo de documento',
            'rut': 'Número de documento',
            'telefono': 'Teléfono',
        }
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': SELECT_CLASS}),
            'rut': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'telefono': forms.TextInput(attrs={'class': FIELD_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
