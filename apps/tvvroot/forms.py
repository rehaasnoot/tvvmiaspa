from django.db import models
from django import forms
from django.forms import Form, ModelForm, ChoiceField, ModelChoiceField
from django.contrib.admin import ModelAdmin
from .models import Order, Player, Instrument, Music

class AdminOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'player', 'instrument', 'music_pkg', 'midi_track_left_hand', 'midi_track_right_hand', 'midi_track_left_foot', 'midi_track_right_foot', 'frames_per_second', 'start_frame', 'end_frame']

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['midi_track_left_hand'].choices = MIDI.objects.filter(music=self.instance.music_pkg.midi_file)

class AdminOrder(ModelAdmin):
    form = AdminOrderForm

class UXOrder(Order):
    track_for_left_hand = models.PositiveSmallIntegerField(default=None)

class OrderCreateForm(Form, ModelForm):
    midi_track_choices = ()
    left_hand = forms.ChoiceField(choices=midi_track_choices)
    class Meta:
        model = UXOrder
#        fields = ['user', 'player', 'instrument', 'music_pkg', 'midi_track_left_hand', 'midi_track_right_hand', 'midi_track_left_foot', 'midi_track_right_foot', 'frames_per_second', 'start_frame', 'end_frame']
        fields = ['user', 'player', 'instrument', 'music_pkg', 'frames_per_second', 'start_frame', 'end_frame']
    def get_midi_track_choices(self):
        for m in [(1,"Track 1"), (2,"TVV Guitar track dummy data")]:
            yield m
    def __init__(self, *args, **kwargs):
        self.midi_track_choices = self.get_midi_track_choices
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        
        self.fields['left_hand'].choices = self.midi_track_choices
        pass

