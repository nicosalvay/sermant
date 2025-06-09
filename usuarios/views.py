from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from usuarios.forms import InfoAdUsuarios, UserForm
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.
def usuarios (request):
    return HttpResponse ("APP USUARIOS") #Retornamos un mensaje de prueba


class ModUsuarios(View):
    template = 'usuarios/usuarios.html'

    def get(self, request):
        form_adicional = InfoAdUsuarios()
        form_user = UserForm ()
        params = {}
        if request.user.is_authenticated:
            # Si el usuario está autenticado, obtenemos sus datos
            try:
                form_adicional = InfoAdUsuarios(instance=request.user.datousuario)
                form_user = UserForm(instance=request.user)
            except Exception as e:
                print(f"Error al obtener los datos del usuario: {e}")
        params['form_user'] = form_user
        params['form_adicional'] = form_adicional  # Pasa el formset al template en el GET
        return render(request, self.template, params)  
        
    def post(self, request):
        params = {}
        form_adicional = InfoAdUsuarios(request.POST, request.FILES, instance=request.user.datousuario)
        form_user = UserForm(request.POST, instance=request.user)
        params['form_user'] = form_user
        params['form_adicional'] = form_adicional
        if form_adicional.is_valid() and form_user.is_valid():
            form_adicional.save()
            form_user.save()
            messages.success(request, 'Los datos se han actualizado correctamente.')
            print("Datos actualizados correctamente")
            return redirect('usuarios')
            #return render(request, self.template,params)
        
        return render(request, self.template, {'form_user': form_user, 'form_adicional': form_adicional})