from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
 
class RegisterView(TemplateView):
    name = 'register_user'
    template_name = 'register.html'
    url = 'register/'
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        context = { "form" : form }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            richie = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account created for {{username}}.'.format(username))
            whereTo = reverse('App')
            return redirect(whereTo)
        return render(request, self.template_name, self.get_context_data())            
    def get_absolute_url(self):
        return reverse(self.name, kwargs={id: self.id})
