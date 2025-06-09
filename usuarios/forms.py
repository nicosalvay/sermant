from django.forms import ModelForm, DateInput, TextInput, Textarea, Select
from usuarios.models import Datousuario
from django import forms
from django.contrib.auth.models import User

class InfoAdUsuarios(ModelForm):
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    fecha_nacimiento = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        required=False
    )
    pais = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    provincia = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    ciudad = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    domicilio = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    codigo_postal = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    telefono = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    celular = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    documento = forms.RegexField(
        regex=r'^\d+$',
        widget=TextInput(attrs={
            'class': 'form-control',  # <--- ¡Añade la clase aquí!
            'inputmode': 'numeric',   # Para teclados móviles
            'pattern': r'^\d+$'       # Para validación HTML5 del lado del cliente
        }),
        required=False,
        error_messages={'invalid': 'Solo se permiten números en este campo.'},
        label="Documento"
    )
    cuit = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    
    class Meta:
        model = Datousuario
        fields = [
            'imagen',
            'fecha_nacimiento',
            'pais',
            'provincia',
            'ciudad',
            'domicilio',
            'codigo_postal',
            'telefono',
            'celular',
            'documento',
            'cuit',
        ]
        
    def __init__(self, *args, **kwargs):
        super(InfoAdUsuarios, self).__init__(*args, **kwargs)

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name.label = "Nombre/s"
    last_name.label = "Apellido/s"
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
