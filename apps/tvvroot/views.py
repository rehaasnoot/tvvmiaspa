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
from django.contrib.auth import authenticate, login, logout
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
   # View configs
GUEST_VIEWS = []
USER_VIEWS = []
ADMIN_VIEWS = []

class TVVLoginView(TemplateView):
    name = 'Login'
    template_name = LOGIN_URL
    url = 'login'
    def get(self, request, *args, **kwargs):
        context = { "menus" : GUEST_VIEWS }
        return render(request, self.template_name, context);
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

class TVVLogoutView(TemplateView):
    name = 'Sign Out'
    template_name = 'registration/loggedout.html'
    url = 'logout'
    def get(self, request, *args, **kwargs):
        context = { "menus" : GUEST_VIEWS }
        return render(request, self.template_name, context);
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logout(request, user)
            return reverse("/")
  
#decorators = [login_required, permission_required, never_cache]

#@method_decorator(decorators, name='dispatch')
#class TVVView(LoginRequiredMixin, TemplateView):
class TVVView(TemplateView):
    name = "TVVView"
    url = 'tvvview'
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            context = { "username" : user.username, "menus": GUEST_VIEWS}
            return render(request, self.template_name, context)            
        return render(request, self.template_name, self.get_context_data())            
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            return render(request, self.template_name, self.get_context_data())            
        return render(request, self.template_name, self.get_context_data())            

class AboutView(TVVView):
    name = 'About'
    template_name = 'about.html'
    url = 'about'

class AppView(TVVView):
    name = 'App'
    template_name = 'app.html'
    url = 'app'
    def get(self, request, *args, **kwargs):
        user = request.user
        admin = False
        if user.is_authenticated and not user.is_anonymous:
            admin = user.is_staff
            menus = GUEST_VIEWS + [TVVLogoutView]
            if admin:
                menus = GUEST_VIEWS + ADMIN_VIEWS + [TVVLogoutView]
            context = { "username" : user.username, "admin" : admin, "menus" : menus}
            return render(request, self.template_name, context)            
        menus = GUEST_VIEWS + [TVVLoginView]
        context = { "username" : user.username, "admin" : admin, "menus" : menus}
        return render(request, self.template_name, context)            

class CreateView(TVVView):
    name = 'Create'
    template_name = 'create.html'
    url = 'create'

class IndexView(TVVView):
    name = 'Index'
    template_name = 'index.html'
    url = 'index'

class PlayerView(TVVView):
    name = 'Player'
    template_name = 'player.html'
    url = 'player'

class PlayerDetail(TVVView):
    name = 'Player'
    template_name = 'playerdetail.html'
    url = 'playerdetail'
    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Player.DoesNotExist:
            raise Http404("Player does not exist")

class VideosView(TVVView):
    name = 'Videos'
    template_name = 'videos.html'
    url = 'videos'
    def get(self, request, *args, **kwargs):
        from .models import Video
        context = { "videos": Video.objects.all() }
        try:
            return render(request, self.template_name, context)
        except Player.DoesNotExist:
            raise Http404("Player does not exist")

class VideoView(TVVView):
    name = 'Video'
    template_name = 'video.html'
    url = 'video'
    def get(self, request, *args, **kwargs):
        from .models import Video
        video_id = kwargs.get('video_id')
        video = Video.objects.get(id=video_id)
        vid_url = video.video_url
        if None == vid_url:  # if not out there on the inna-tubes, use local
            vid_url =  "/media/" + video.video_uri.name
        context = { "title" : video.title, "url": vid_url }
        try:
            return render(request, self.template_name, context)
        except Player.DoesNotExist:
            raise Http404("Player does not exist")

class OrdersView(TVVView):
    name = 'Orders'
    template_name = 'orders.html'
    url = 'orders'
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
    name = 'Order Details'
    template_name = 'orderdetail.html'
    url = 'order'

class TVVAdminView():
    name = 'Admin View'
    template_name = None
    url = 'admin'

class TVVGraphQLView():
    name = 'GraphiQL View'
    template_name = None
    url = 'graphql'


#from ..urls import admin
#class AdminView(admin.site.urls):
#    pass

GUEST_VIEWS = [AboutView, VideosView]
ADMIN_VIEWS = [ TVVAdminView, TVVGraphQLView ]

