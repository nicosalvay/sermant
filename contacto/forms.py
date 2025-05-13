from django import forms
from django.forms import ModelForm
from contacto.models import Consulta
from captcha.fields import CaptchaField

class ConsultaForm(ModelForm):
    captcha = CaptchaField()
    #Meta es una clase interna que se utiliza para definir metadatos sobre el formulario.
    #En este caso, se está utilizando para especificar el modelo que se va a utilizar (Contacto) y los campos que se van a incluir en el formulario.
    class Meta:
        model = Consulta
        fields = [
            'nombre',
            'apellido',
            'cod_area',
            'telefono',
            'email',
            'mensaje',
        ]

    def send_email(self):
        # self.cleaned_data es un diccionario que contiene los datos del formulario después de haber sido validados.
        nombre = self.cleaned_data['nombre']
        apellido = self.cleaned_data['apellido']
        cod_area = self.cleaned_data['cod_area']
        telefono = self.cleaned_data['telefono']
        email = self.cleaned_data['email']
        mensaje = self.cleaned_data['mensaje']
        # AGREGAR LÓGICA DE ENVIO DE MAIL