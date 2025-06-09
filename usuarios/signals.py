from django.db.models.signals import post_save  # Importa la señal 'post_save', que se emite después de guardar un modelo.
from django.dispatch import receiver      # Importa el decorador 'receiver', que conecta una función a una señal específica.
from django.contrib.auth.models import User  # Importa el modelo 'User' de Django, que representa la información básica de los usuarios.
from usuarios.models import Datousuario    # Importa el modelo 'Datosusuario' de tu aplicación 'usuarios', que contiene información adicional sobre los usuarios.

@receiver(post_save, sender=User)         # Este decorador indica que la función 'create_datosusuario' se ejecutará cuando se emita la señal 'post_save' para el modelo 'User'.
def create_datosusuario(sender, instance, created, **kwargs):
    # 'sender': El modelo que envió la señal (en este caso, 'User').
    # 'instance': La instancia específica del modelo 'User' que se acaba de guardar.
    # 'created': Un valor booleano que es True si la instancia fue recién creada, y False si fue actualizada.
    # '**kwargs': Argumentos de palabra clave adicionales que se pueden pasar a la señal.
    if created:  # Verifica si el usuario ('User') fue recién creado.
        Datousuario.objects.create(usuario=instance)  # Si fue creado, crea un nuevo registro en el modelo 'Datosusuario'.
                                                      # Asigna el usuario recién creado ('instance') al campo 'usuario' del nuevo 'Datosusuario'.
        print("Se han creado los datos ")              # Imprime un mensaje en la consola indicando que los datos adicionales fueron creados.


@receiver(post_save, sender=User)
def update_datosusuario(sender, instance, created, **kwargs):
    if created == False:  # Si el usuario NO es nuevo (fue actualizado)
        instance.datousuario.save()  # Guarda los datos relacionados en Datosusuario
        print("Se han actualizado los datos ")  # Imprime un mensaje en la consola indicando que los datos fueron actualizados.