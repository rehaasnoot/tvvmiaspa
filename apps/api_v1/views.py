import os
from rest_framework.views import APIView
from django.contrib.auth.views import TemplateView
from django.http import JsonResponse
from ..tvvroot.models import Order, MIDI, InstrumentMap
from apps.settings import MEDIA_URL, MEDIA_ROOT
from .blagent_api import TVVBlagent

#baseuri = 'api/v1/'
baseuri = 'api/v1/'
InputInt = '<int:order_id>'

class MIDIUtils():
    def midi_tracks(self, classname, track_values):
        """
        Note: track_values expects to be one of:
            None - for woodwind, guitar, etc.
            [int, int] - for keyboard, marimba, etc.
            [int, int, int, int] - for drum kits
        """
        im = InstrumentMap.objects.filter(classname=classname)
        il = im[0].limbs
        tracks = None
        if None != il:
            if isinstance(track_values, list):
                left_hand_track = None
                right_hand_track = None
                left_foot_track = None
                right_foot_track = None
                for t in track_values:
                    if None != t:
                        if None == tracks:
                            tracks = []
                        tracks.append(t)
            else:
                tracks = [track_values]
        return tracks
    def track_values(self, midi):
        tracks = None
        midi_objects = MIDI.objects.filter(music=midi)
        for midi_object in midi_objects:
            if None != midi_object:
                track_id = midi_object.track_number
                if None != track_id and track_id > 0:
                    if None == tracks:
                        tracks = []
                    tracks.append(track_id)
        return tracks
    def processOrder(self, orderId):
        order = Order.objects.get(id=orderId)
        fps = order.frames_per_second
        frame_start = order.start_frame
        frame_end = order.end_frame
        player = order.player
        player_name = player.name
        blend = player.blend_file
        player_blend_file = os.path.join(MEDIA_ROOT, blend.name)
        music_pkg = order.music_pkg
        midi = music_pkg.midi_file
        midi_file = os.path.join(MEDIA_ROOT, midi.name)
        instrument = order.instrument
        instrument_blend = instrument.blend_file
        instrument_file = os.path.join(MEDIA_ROOT, instrument_blend.name)
        instrument_name = instrument.name
        blagent = TVVBlagent()
        cn = instrument.classname
        track_id_s = self.midi_tracks(cn, self.track_values(music_pkg))
        blagent.assemble(fps, track_id_s, player_name, instrument_name, player_blend_file, 
                            instrument_file, cn, midi_file, frame_start, frame_end)
        return True

class ApiView(APIView, MIDIUtils):
    name = 'ApiView'
    def getInt(self, uri):
        return self.url + uri + InputInt

class PingView(ApiView):
    name = 'PingView'
    url = baseuri + 'ping/'
    def get(self, request, *args, **kwargs):
        context = { "status_code" : 200, "status_description" : "OK" }
        return JsonResponse(context)     
class OrderView(ApiView):
    name = 'OrderView'
    url = baseuri + 'getorder/'
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(deliverable=None)
        count = orders.__len__()
        orderId = orders[count -1].pk
        context = { "order_id" : orderId }
        return JsonResponse(context)     
class ProcessView(ApiView, MIDIUtils):
    name = 'ProcessView'
    url = baseuri + 'process/'
    def post(self, request, *args, **kwargs):
        orderId = request.data.get('order_id')
        if self.processOrder(orderId):
            context = { "orderId" : orderId, "status" : "OK" }
        else:
            context = { "orderId" : orderId, "status" : "Failed" }
        return JsonResponse(context)

