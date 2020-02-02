import os
from django import forms
from django.shortcuts import render, redirect, reverse
from apps.settings import LOGIN_URL, ROOT_URL
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_safe
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, ModelFormMixin
import requests
import datetime
#from apps.settings import MEDIA_URL, MEDIA_ROOT
from .models import Order, Player, Instrument, InstrumentMap, Music, MIDI, FramesPerSecond
from .forms import AdminOrderForm, OrderCreateForm
from apps.api_v1.views import MIDIUtils

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
class TVVView(LoginRequiredMixin, CreateView, TemplateView):
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
            menus = GUEST_VIEWS
            orders = None
            try:
                orders = Order.objects.filter(user=user.id)
            except Order.DoesNotExist:
                pass
            if None != orders:
                menus = GUEST_VIEWS + USER_VIEWS + [ OrdersView ]
            else:
                menus = GUEST_VIEWS + USER_VIEWS
            if admin:
                menus = GUEST_VIEWS + USER_VIEWS + [ OrdersView ] + ADMIN_VIEWS
            menus += [ TVVLogoutView ]
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
            vid_url =  MEDIA_URL + video.video_uri.name
        context = { "title" : video.title, "url": vid_url, "media_type": video.codec }
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
            orders = Order.objects.filter(user=user)
            if None != orders and orders.__len__() > 0:
                ctxOrders = []
                if orders.__len__() > 1:
                    for o in orders:
                        ctxOrders.append(o)
                else:
                    ctxOrders.append(orders[0])
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
                "description": order.description,
                "start_frame": order.start_frame, 
                "end_frame": order.end_frame,
                "midi_track": [order.midi_track_left_hand, order.midi_track_right_hand, order.midi_track_left_foot, order.midi_track_right_foot]

                 }
            return render(request, self.template_name, context)            
        return render(request, self.template_name, self.get_context_data())    

class OrderCreateView(TVVView):
    name = 'Order Create'
    model = Order
    url = '/order/create'
    template_name = 'forms/order_form.html'
    form_class = OrderCreateForm
    #aux_form_class = MIDIListForm
    fields = ['user', 'player', 'instrument', 'music_pkg', 'frames_per_second', 'start_frame', 'end_frame']
    # ui-selection fields
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            form = OrderCreateForm()
            music_pkg_pk = None # request.GET['music_pkg']
            if None != music_pkg_pk:
                music_pkg = Music.objects.get(pk=music_pkg_pk)
                midi = MIDI.objects.filter(music=music_pkg_pk)
                midi_choices = []
                for m in midi:
                    midi_choices.append( (m.track_number, m.name) )
                form.fields['left_hand'].choices = mid_choices
            return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            post = request.POST
            player = Player.objects.get(pk=post['player'])
            instrument = Instrument.objects.get(pk=post['instrument'])
            music_pkg = Music.objects.get(pk=post['music_pkg'])
            frames_per_second = FramesPerSecond.objects.get(pk=post['frames_per_second'])
            start_frame = post['start_frame']
            end_frame = post['end_frame']
            description = player.name + " playing " + music_pkg.title + " on " + instrument.name
            new_order = Order.objects.create(
                player=player, 
                instrument=instrument, 
                music_pkg = music_pkg,
                user = user,
                frames_per_second = frames_per_second,
                start_frame = start_frame,
                end_frame = end_frame,
                description = description)
        return redirect("/")

class OrderPurchaseView(TVVView, MIDIUtils):
    name = 'Order Purchase'
    template_name = 'orderdetail.html'
    url = '/order/purchase/'
    def get(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_anonymous:
            from .models import Order
            order_id = kwargs.get('pk')
            if self.processOrder(order_id):
                context = { 
                    "description": order.description,
                    "fps" : fps,
                    "start_frame": frame_start, 
                    "end_frame": frame_end,
                    "player": order.player.name,
                    "instrument": order.instrument.name,
                    "midi_tracks": track_id_s,
                    "class_name" : cn
                     }
                return render(request, self.template_name, context)            
        return render(request, self.template_name, self.get_context_data())

class TVVBlagentView(TVVView):
    name = 'Blender Agent'
    template_name = 'blagent.html'
    url = '/blagent'    
    def get(self, request, *args, **kwargs):
        user = request.user
        context = { 'richie': 'richie' }
        return context
#        return render(request, self.template_name, context)            
        
class TVVAdminView():
    name = 'Admin View'
    template_name = None
    url = '/admin'

class TVVGraphQLView():
    name = 'GraphiQL View'
    template_name = None
    url = '/graphql'

GUEST_VIEWS = [AboutView, VideosView]
USER_VIEWS = [OrderCreateView]
ADMIN_VIEWS = [ TVVBlagentView, TVVAdminView, TVVGraphQLView ]

