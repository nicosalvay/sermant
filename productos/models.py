from django.db import models
from django.utils.html import format_html

# Create your models here.

class Producto(models.Model):
    producto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField('Fecha de publicación')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=[('Activo', 'Activo'), ('No activo', 'No activo')])
    imagen = models.ImageField(upload_to="productos/%Y/%m/%d", blank=True, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name="productos")

    def __str__ (self, ):
        return self.producto

    def estado_de_producto (self):
        if self.estado == "No activo":
            return format_html('<span style="color:white; background-color:#601515;padding:7px;">{}</span>', self.estado)
        else:
            return format_html ('<span style="color:white;background-color:#3E92CC;padding:7px;">{}</span>',self.estado)


class Categoria(models.Model):
    activo = "Activo"
    no_activo = "No activo"
    estado_categoria = [
        (activo, "Activo"),
        (no_activo, "No activo"),
    ]

    nombre = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    estado = models.CharField(max_length=10, choices=estado_categoria, default='No activo')

    def __str__(self):
        return self.nombre
    
class ImgProducto(models.Model):
    estado = models.CharField(max_length=10, choices=[('Activo', 'Activo'), ('No activo', 'No activo')])
    imagen = models.ImageField(upload_to="img_productos/%Y/%m/%d", blank=True, null=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name="imagenes")