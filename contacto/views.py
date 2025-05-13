from django.shortcuts import render
from django.views.generic import View
from django.views.generic import FormView
from contacto.forms import ConsultaForm

# Create your views here.
class Contacto(FormView):
    template_name = 'contacto/contacto.html'
    form_class = ConsultaForm
    #success_url contiene la URL a la que se redirigirá al usuario después de que el formulario se haya enviado correctamente.
    success_url = 'mensaje_enviado'
    #si el formulario no es válido, se redirige a la misma página.
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    #form_valid es un método que se llama cuando el formulario es válido. Es un método de la clase FormView.
    def form_valid(self, form):
        form.save()
        form.send_email()
        return super().form_valid(form)

class MensajeEnviado(View):
    template_name = 'contacto/mensaje_enviado.html'

    def get(self, request):
        params = {}
        params['mensaje'] = 'Su mensaje ha sido enviado correctamente.'
        return render(request, self.template_name, params)