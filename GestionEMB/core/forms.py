from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PerfilUsuario


class LoginForm(forms.Form):
    """Formulario de inicio de sesión"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Usuario o Email',
            'id': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Contraseña',
            'id': 'password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id': 'remember'
        })
    )


class CrearUsuarioForm(forms.Form):
    """Formulario para crear un nuevo usuario"""
    username = forms.CharField(
        max_length=150,
        label='Nombre de Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: jdoe'
        })
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'usuario@ejemplo.com'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        label='Nombre(s)',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'John'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        label='Apellido(s)',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Doe'
        })
    )
    password = forms.CharField(
        min_length=8,
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mínimo 8 caracteres'
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Repite la contraseña'
        })
    )
    rol = forms.ChoiceField(
        choices=PerfilUsuario.ROLES,
        label='Rol',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    afiliacion = forms.CharField(
        max_length=200,
        required=False,
        label='Afiliación',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Universidad, Institución, etc.'
        })
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+57 300 123 4567'
        })
    )
    
    def clean_username(self):
        """Validar que el username no exista"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username
    
    def clean_email(self):
        """Validar que el email no exista"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data


class EditarUsuarioForm(forms.ModelForm):
    """Formulario para editar un usuario existente"""
    rol = forms.ChoiceField(
        choices=PerfilUsuario.ROLES,
        label='Rol',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    afiliacion = forms.CharField(
        max_length=200,
        required=False,
        label='Afiliación',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Universidad, Institución, etc.'
        })
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+57 300 123 4567'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Nombre(s)',
            'last_name': 'Apellido(s)',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que el username no sea editable para evitar problemas
        self.fields['username'].disabled = True
    
    def clean_email(self):
        """Validar que el email no esté en uso por otro usuario"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email


class EditarPerfilForm(forms.ModelForm):
    """Formulario para que el usuario edite su propio perfil"""
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+57 300 123 4567'
        })
    )
    afiliacion = forms.CharField(
        max_length=200,
        required=False,
        label='Afiliación',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Universidad, Institución, etc.'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellido(s)',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }
    
    def clean_email(self):
        """Validar que el email no esté en uso por otro usuario"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email