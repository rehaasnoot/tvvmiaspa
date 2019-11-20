from django.shortcuts import render, redirect
from ..settings import LOGIN_URL, ROOT_URL
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_safe
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import datetime


def loginViewF(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect(to='/app')
    return render('Login Failed')
    
@require_safe
@never_cache
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

#from django.http import HttpResponseNotFound
from django.http import Http404
from apps.tvvroot.models import Player

#class Http404(TemplateView):
#    template_name = "404.html"
    
class TVVLoginView(TemplateView):
    template_name = 'registration/login.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name);
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/app')
        raise Http404('Login Failed')

decorators = [login_required, permission_required, never_cache]

#@method_decorator(decorators, name='dispatch')
#class TVVView(LoginRequiredMixin, TemplateView):
class TVVView(TemplateView):
    template_name = None
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            return render(request, self.template_name, self.get_context_data())            
        return render(request, self.template_name, self.get_context_data())            
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            return render(request, self.template_name, self.get_context_data())            
        return render(request, self.template_name, self.get_context_data())            
    
class IndexView(TVVView):
    template_name = 'index.html'

class AppView(TVVView):
    template_name = 'app.html'

class CreateView(TVVView):
    template_name = 'create.html'

class AboutView(TVVView):
    template_name = 'about.html'

class PlayerView(TVVView):
    template_name = 'player.html'

class PlayerDetail(TVVView):
    player_id = 1
    def get(self, request, *args, **kwargs):
        try:
            return render(request, 'playerdetail.html', {})
        except Player.DoesNotExist:
            raise Http404("Player does not exist")
