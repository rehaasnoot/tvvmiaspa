from django.shortcuts import render, redirect, reverse
import requests
from apps.settings import LOGIN_URL, ROOT_URL, BLAGENT_URI
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
from apps.settings import BLAGENT_URI
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Order, Player, Instrument, Music

@require_safe
@never_cache
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def fibonacci(n):
    fib = 1
    previousFib = 0
    while fib < n:
        yield fib
        previousFib, fib = fib, previousFib + fib

def WWWfibonacci(request, n):
#    n = request.get('n')
    html = "<html>No 'n'. Doing nothing.<body>"
    if None != n:
        html = "<html><body>"
        for fib in fibonacci(int(n)):
            html += "{},".format(str(fib))
        html += "</body></html>"
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
    template_name = 'login.html'
    url = '/login'
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
                return redirect(TVVAdminView.url)
            return redirect(OrdersView.get_absolute_url())
        raise Http404("Login Failed")

class TVVLogoutView(TemplateView):
    name = 'Logout'
    template_name = 'loggedout.html'
    url = '/logout'
    def get(self, request, *args, **kwargs):
        user = request.user
        if user is not None:
            logout(request)
        return redirect(AppView.url)
  
#decorators = [login_required, permission_required, never_cache]

#@method_decorator(decorators, name='dispatch')
#class TVVView(LoginRequiredMixin, TemplateView):
class TVVView(TemplateView):
    name = "TVVView"
    url = '/tvvview'
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            context = { "username" : user.username, "menus": GUEST_VIEWS}
            return render(request, self.template_name, context)            
        return render(request, self.template_name)            
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            return render(request, self.template_name)            
        return render(request, self.template_name)            

class AboutView(TVVView):
    name = 'About'
    template_name = 'about.html'
    url = '/about'

class AppView(TVVView):
    name = 'App'
    template_name = 'app.html'
    url = '/app'
    def get(self, request, *args, **kwargs):
        user = request.user
        admin = False
        menus = GUEST_VIEWS
        if user.is_authenticated and not user.is_anonymous:
            admin = user.is_staff
            menus = GUEST_VIEWS + [OrderCreate, TVVLogoutView]
            orders = None
            try:
                orders = Order.objects.get(user=user.id)
            except Order.DoesNotExist:
                pass
            if None != orders:
                menus = GUEST_VIEWS + USER_VIEWS + [TVVLogoutView]
            if admin:
                menus = GUEST_VIEWS + USER_VIEWS + ADMIN_VIEWS + [TVVLogoutView]
            context = { "username" : user.username, "admin" : admin, "menus" : menus}
            return render(request, self.template_name, context)            
        menus = GUEST_VIEWS + [TVVLoginView]
        context = { "username" : user.username, "admin" : admin, "menus" : menus}
        return render(request, self.template_name, context)            

class IndexView(TVVView):
    name = 'Index'
    template_name = 'index.html'
    url = '/index'

class PlayerView(TVVView):
    name = 'Player'
    template_name = 'player.html'
    url = '/player'

class PlayerDetail(TVVView):
    name = 'Player'
    template_name = 'playerdetail.html'
    url = '/playerdetail'
    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Player.DoesNotExist:
            raise Http404("Player does not exist")

class VideosView(TVVView):
    name = 'Videos'
    template_name = 'videos.html'
    url = '/videos'
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
    url = '/video'
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
    url = '/orders'
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            ctxOrders = None
            orders = Order.objects.get(user=user)
            if None != orders:
                if isinstance(orders, list):
                    ctxOrders = []
                    ctxOrders.append(orders)
                else:
                    ctxOrders = [orders]
            context = { 
                "username" : user.username,
                "orders" : ctxOrders
             }
            return render(request, self.template_name, context)            
        return render(request, self.template_name, self.get_context_data())            
class OrderDetailView(TVVView):
    name = 'order_detail'
    template_name = 'orderdetail.html'
    url = '/order/detail/'
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            from .models import Order
            order_id = kwargs.get('pk')
            order = Order.objects.get(id=order_id)
            context = { 
                "description": order.descr(),
                "start_frame": order.start_frame, 
                "end_frame": order.end_frame
                 }
            return render(request, self.template_name, context)            
        return render(request, self.template_name, self.get_context_data())    
   
class OrderCreate(TVVView):
    name = 'Order Create'
    model = Order
    url = '/order/create'
    template_name = 'order_form.html'
    fields = ['user', 'player', 'instrument', 'music_pkg', 'start_frame', 'end_frame']
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            if None == user.email:
                return redirect(reverse("register_user"))
        players = Player.objects.all()
        instruments = Instrument.objects.all()
        music = Music.objects.all()
        start_frame = 1
        end_frame = 250
        context = {
            "players": players,
            "instruments": instruments,
            "music": music,
            "start_frame": start_frame,
            "end_frame": end_frame
            }
        return render(request, self.template_name, context)       
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
class OrderUpdate(LoginRequiredMixin, UpdateView):
    name = 'Order Update'
    model = Order
    url = '/order/update'
    fields = ['player', 'instrument', 'music_pkg', 'start_frame', 'end_frame']
class OrderDelete(LoginRequiredMixin, DeleteView):
    name = 'Order Delete'
    model = Order
    url = '/order/delete'
    success_url = reverse_lazy('orders')

class TVVBlagentView(TVVView):
    name = 'Blender Agent'
    template_name = 'blagent.html'
    url = '/blagent'
    def get(self, request, *args, **kwargs):
        frame_start = requests.get(BLAGENT_URI + "getframestart").json().get('frame_start')
        frame_end = requests.get(BLAGENT_URI + "getframeend").json().get("frame_end")      
        player_name = requests.get(BLAGENT_URI + "getplayername").json().get("player_name")      
        instrument_name = requests.get(BLAGENT_URI + "getinstrumentname").json().get("instrument_name")      
        midi_file_name = requests.get(BLAGENT_URI + "getmidifilename").json().get("midi_file_name")      
        midi_track = requests.get(BLAGENT_URI + "getmiditrack").json().get("midi_track")      
        context = { "blagent" : "blender agent api",
                    "frame_start": frame_start,
                    "frame_end": frame_end,
                    "player_name": player_name,
                    "instrument_name": instrument_name,
                    "midi_file_name": midi_file_name,
                    "midi_track": midi_track

        }
        return render(request, self.template_name, context)         
    
class TVVAdminView():
    name = 'Admin View'
    template_name = None
    url = '/admin'

class TVVGraphQLView():
    name = 'GraphiQL View'
    template_name = None
    url = '/graphql'

GUEST_VIEWS = [AboutView, VideosView]
USER_VIEWS = [OrdersView, OrderCreate]
ADMIN_VIEWS = [ TVVBlagentView, TVVAdminView, TVVGraphQLView ]

