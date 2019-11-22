from django.shortcuts import render, redirect
from django.contrib.auth.views import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
 
class RegisterView(TemplateView):
    template_name = 'register.html'
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        context = { "form" : form }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {{username}}.')
            return redirect('/app')
            
        return render(request, self.template_name, self.get_context_data())            

def registerUser(response):
    if "POST" == response.method:
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(response, 'register.html', { "form": form })