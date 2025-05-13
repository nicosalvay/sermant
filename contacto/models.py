from django.db import models
import datetime
from django.utils.html import format_html
from datetime import datetime

# Create your models here.
class Consulta(models.Model):
    CONTESTADA = 'Contestada'
    NOCONTESTADA = 'No Contestada'
    ENPROCESO = 'En Proceso'
    ESTADOS = (
        (CONTESTADA, 'Contestada'),
        (NOCONTESTADA, 'No Contestada'),
        (ENPROCESO, 'En Proceso'),
    )


    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cod_area = models.CharField(max_length=5)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    mensaje = models.TextField()
    estado_respuesta = models.CharField(max_length=20, choices=ESTADOS, default=NOCONTESTADA)
    fecha_contacto = models.DateTimeField(default=datetime.now, blank=True,editable=True)

    def __str__(self):
        return self.nombre + " " + self.apellido
    
    def estado_de_respuesta(self):
        if self.estado_respuesta == 'Contestada':
            return format_html('<span style="background-color:green; color:#fff; padding:5px;">{}</span>', self.estado_respuesta,)
        elif self.estado_respuesta == 'No Contestada':
            return format_html('<span style="background-color:red; color:#fff; padding:5px;">{}</span>', self.estado_respuesta,)
        elif self.estado_respuesta == 'En Proceso':
            return format_html('<span style="background-color:orange; color:#fff; padding:5px;">{}</span>', self.estado_respuesta,)
    
class Respuesta(models.Model):
    #Definición de los Campos del Modelo:
    consulta = models.ForeignKey(Consulta(), blank=True, null=True, on_delete=models.CASCADE)
    respuesta = models.TextField(blank=False, null=False)
    fecha_respuesta = models.DateField(default=datetime.now, blank=True, editable=True)

    def create_mensaje(self):
        contacto_cambio_estado = Consulta.objects.get(id=self.consulta.id)
        contacto_cambio_estado.estado_respuesta = 'Contestada'
        contacto_cambio_estado.save()
        # AGREGAR LÓGICA DE ENVIO DE MAIL
        
    #save es un método que se llama cuando se guarda el objeto en la base de datos. Es un método de la clase Model.
    def save(self, *args, **kwargs):
        #Esta parte del código se encarga de determinar si estás creando una nueva respuesta o modificando una que ya existe,
        #y le indica a la base de datos que haga la operación correcta (crear o actualizar).
        self.create_mensaje()
        force_update = False
        if self.id:
            force_update = True
        #Aquí se llama al método save() de la clase padre (models.Model) para guardar el objeto en la base de datos.
        super(Respuesta, self).save(force_update=force_update)


