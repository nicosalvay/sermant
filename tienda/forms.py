from django import forms
from django.forms import ModelForm, DateInput, TextInput, Textarea, Select
from django.forms import inlineformset_factory
from productos.models import Producto,Categoria, ImgProducto

class CargaProducto(ModelForm):
    categoria = forms.ModelChoiceField(
    queryset=Categoria.objects.all(),
    empty_label="Seleccione una categoría",
    widget=Select(attrs={'class': 'form-control'}))
    producto = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(widget=TextInput(attrs={'class': 'form-control'}))
    fecha_publicacion = forms.DateField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    precio = forms.DecimalField(widget=TextInput(attrs={'class': 'form-control'}))
    estado = forms.ChoiceField(
    choices=[('Activo', 'Activo'), ('No activo', 'No activo')],
    widget=Select(attrs={'class': 'form-control'}))
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Producto
        fields = [
            'categoria',
            'producto',
            'descripcion',
            'stock',
            'fecha_publicacion',
            'precio',
            'estado',
            'imagen',
        ]
    def __init__(self, *args, **kwargs):
        super(CargaProducto, self).__init__(*args, **kwargs)

ImagenesProductoFormSet = inlineformset_factory(Producto, ImgProducto, fields=('imagen','estado',), extra=3, can_delete=True)
# 'extra=3' indica que se mostrarán 3 formularios vacíos para subir imágenes inicialmente.
# 'can_delete=True' permite eliminar imágenes existentes al editar el producto.