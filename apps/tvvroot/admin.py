from django.contrib import admin
from .models import Instrument, Music, Order, Player, UserPhoto

admin.site.register(UserPhoto)
admin.site.register(Instrument)
admin.site.register(Music)
admin.site.register(Order)
admin.site.register(Player)