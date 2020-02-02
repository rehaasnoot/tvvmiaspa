from django.contrib import admin
from .models import Instrument, Music, MIDI, Order, Player, UserPhoto, Video, FramesPerSecond, InstrumentMap

admin.site.register(UserPhoto)
admin.site.register(Instrument)
admin.site.register(Music)
admin.site.register(MIDI)
admin.site.register(Order)
admin.site.register(Player)
admin.site.register(Video)
admin.site.register(FramesPerSecond)
admin.site.register(InstrumentMap)