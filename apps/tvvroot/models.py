
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from uuid import uuid1
from ..settings import UPLOAD_USER_IMAGE, UPLOAD_INSTRUMENT_IMAGE, UPLOAD_INSTRUMENT_BLEND, UPLOAD_PLAYER_IMAGE, UPLOAD_PLAYER_BLEND, UPLOAD_MUSIC_MIDI, UPLOAD_MUSIC_AUDIO

class UserPhoto(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    photos = ProcessedImageField(upload_to=UPLOAD_USER_IMAGE,
                                       processors=[ResizeToFill(300, 300)],
                                       format='JPEG',
                                       options={'quality': 90})

class Instrument(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    blend_file = models.FileField(upload_to=UPLOAD_INSTRUMENT_BLEND, default=None, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=UPLOAD_INSTRUMENT_IMAGE, default=None, blank=True, null=True)

class Player(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    blend_file = models.FileField(upload_to=UPLOAD_PLAYER_BLEND, default=None, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=UPLOAD_PLAYER_IMAGE, default=None, blank=True, null=True)
    
class Music(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    title = models.CharField(max_length=100)
    midi = models.FileField(upload_to=UPLOAD_MUSIC_MIDI, default=None, blank=True, null=True)
    audio = models.FileField(upload_to=UPLOAD_MUSIC_AUDIO, default=None, blank=True, null=True)

class Order(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    description = models.CharField(max_length=512, default=None, blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    music_pkg = models.ForeignKey(Music, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField()
    in_progress = models.BooleanField()
    progress = models.PositiveSmallIntegerField(null=True)
    deliverable = models.URLField(default=None, blank=True, null=True)
    def __str__(self):
        return "For: {}, {} -- {} playing {} on {}...".format(self.user.last_name, self.user.first_name, self.player.name, self.music_pkg.title, self.instrument.name) 
