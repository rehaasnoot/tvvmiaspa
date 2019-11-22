from django.shortcuts import render, redirect, reverse
from ..settings import LOGIN_URL, ROOT_URL
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
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
    template_name = LOGIN_URL
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name);
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            loggedIn = login(request, user)
            if user.is_superuser:
                return redirect("/admin")
            return reverse("orders")
        raise Http404("Login Failed")

decorators = [login_required, permission_required, never_cache]

#@method_decorator(decorators, name='dispatch')
#class TVVView(LoginRequiredMixin, TemplateView):
class TVVView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            context = { "username" : user.username }
            return render(request, self.template_name, context)            
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
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            admin = user.is_staff
            context = { "username" : user.username, "admin" : admin}
            return render(request, self.template_name, context)            
        return render(request, self.template_name, self.get_context_data())            

class CreateView(TVVView):
    template_name = 'create.html'

class AboutView(TVVView):
    template_name = 'about.html'

class PlayerView(TVVView):
    template_name = 'player.html'

class PlayerDetail(TVVView):
    player_id = 1
    template_name = 'playerdetail.html'
    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Player.DoesNotExist:
            raise Http404("Player does not exist")

class VideosView(TVVView):
    template_name = 'videos.html'
    def get(self, request, *args, **kwargs):
        from .models import Video
        context = { "videos": Video.objects.all() }
        try:
            return render(request, self.template_name, context)
        except Player.DoesNotExist:
            raise Http404("Player does not exist")

class VideoView(TVVView):
    template_name = 'video.html'
    def get(self, request, *args, **kwargs):
        from .models import Video
        video_id = kwargs.get('video_id')
        video = Video.objects.get(id=video_id)
        context = { "video": video }
        try:
            return render(request, self.template_name, context)
        except Player.DoesNotExist:
            raise Http404("Player does not exist")

class OrderView(TVVView):
    template_name = 'order.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            
            context = { 
                "username" : user.username,
                "order" : user.orders
             }
            return render(request, self.template_name, context)            
        return render(request, self.template_name, self.get_context_data())            

class OrderDetailView(TVVView):
    template_name = 'orderdetail.html'

