from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from uuid import uuid1
from apps.settings import UPLOAD_USER_IMAGE, UPLOAD_INSTRUMENT_IMAGE, UPLOAD_INSTRUMENT_BLEND, UPLOAD_PLAYER_IMAGE, UPLOAD_PLAYER_BLEND, UPLOAD_MUSIC_MIDI, UPLOAD_MUSIC_AUDIO, UPLOAD_VIDEO

TVV_THUMBNAIL_ASPECT_X = 300
TVV_THUMBNAIL_ASPECT_Y = 300
TVV_THUMBNAIL_QUALITY = 99
TVV_THUMBNAIL_FORMAT = 'JPEG'


class UserPhoto(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    photos = ProcessedImageField(upload_to=UPLOAD_USER_IMAGE,
                                       processors=[ResizeToFill(TVV_THUMBNAIL_ASPECT_X, TVV_THUMBNAIL_ASPECT_Y)],
                                       format=TVV_THUMBNAIL_FORMAT,
                                       options={'quality': TVV_THUMBNAIL_QUALITY})

class Instrument(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    blend_file = models.FileField(upload_to=UPLOAD_INSTRUMENT_BLEND, default=None, blank=True, null=True)
    thumbnail_orig = models.ImageField(upload_to=UPLOAD_INSTRUMENT_IMAGE, default=None, blank=True, null=True)
    thumbnail = ImageSpecField(source='thumbnail_orig', processors=[ResizeToFill(TVV_THUMBNAIL_ASPECT_X, TVV_THUMBNAIL_ASPECT_Y)],
                    format=TVV_THUMBNAIL_FORMAT, options={'quality': TVV_THUMBNAIL_QUALITY})

    def __str__(self):
        return "{}".format(self.name) 

class Player(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    blend_file = models.FileField(upload_to=UPLOAD_PLAYER_BLEND, default=None, blank=True, null=True)
    thumbnail_orig = models.ImageField(upload_to=UPLOAD_PLAYER_IMAGE, default=None, blank=True, null=True)
    thumbnail = ImageSpecField(source='thumbnail_orig', processors=[ResizeToFill(TVV_THUMBNAIL_ASPECT_X, TVV_THUMBNAIL_ASPECT_Y)],
                    format=TVV_THUMBNAIL_FORMAT, options={'quality': TVV_THUMBNAIL_QUALITY})
    def __str__(self):
        return "{} on {}".format(self.name, self.description) 
    
class Music(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    title = models.CharField(max_length=100)
    midi = models.FileField(upload_to=UPLOAD_MUSIC_MIDI, default=None, blank=True, null=True)
    audio = models.FileField(upload_to=UPLOAD_MUSIC_AUDIO, default=None, blank=True, null=True)
    def __str__(self):
        return "{}".format(self.title) 

class Video(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    title = models.CharField(max_length=100)
    video_uri = models.FileField(upload_to=UPLOAD_VIDEO, default=None, blank=True, null=True)
    video_url = models.URLField(default=None, blank=True, null=True)
    codec = models.CharField(max_length=64, default=None, blank=True, null=True)
    def __str__(self):
        return "{} format {}".format(self.title, self.codec) 

class Order(models.Model):
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    description = models.CharField(max_length=512, default=None, blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    music_pkg = models.ForeignKey(Music, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_frame = models.PositiveSmallIntegerField(default=0)
    end_frame = models.PositiveSmallIntegerField(default=250)
    is_complete = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    progress = models.PositiveSmallIntegerField(default=0)
    deliverable = models.URLField(default=None, blank=True, null=True)
    def __str__(self):
        return "For: {}, {} -- {} playing {} on {}...".format(self.user.last_name, self.user.first_name, self.player.name, self.music_pkg.title, self.instrument.name) 
    def descr(self):
        return "{},{}-{} playing {} on {}".format(self.user.last_name, self.user.first_name, self.player.name, self.music_pkg.title, self.instrument.name) 
    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

class Blender(models.Model):
    BLENDER_STATUS_PENDING = "PENDING"
    BLENDER_STATUS_REQUESTED = "REQUESTED"
    BLENDER_STATUS_STARTING = "STARTING"
    BLENDER_STATUS_RUNNING = "RUNNING"
    BLENDER_STATUS_ENDING = "ENDING"
    BLENDER_STATUS_ENDED = "ENDED"
    BLENDER_STATUS_CHOICES = (
        (BLENDER_STATUS_PENDING, 'Blender agent pending'),
        (BLENDER_STATUS_REQUESTED, 'Blender agent requested'),
        (BLENDER_STATUS_STARTING, 'Blender agent starting'),
        (BLENDER_STATUS_RUNNING, 'Blender agent running'),
        (BLENDER_STATUS_ENDING, 'Blender agent ending'),
        (BLENDER_STATUS_ENDED, 'Blender agent ending'),
    )
    uuid = models.UUIDField(max_length=64, verbose_name=u"databasekey", default=uuid1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pid = models.IntegerField(default=-1)
    status = models.CharField(max_length=32, verbose_name=u"status", choices=BLENDER_STATUS_CHOICES, default=BLENDER_STATUS_PENDING)
    progress = models.PositiveSmallIntegerField(default=0)
    frame_start = models.PositiveIntegerField(default=1)
    frame_end = models.PositiveIntegerField(default=250)
    def __str__(self):
        return "Order Process: {} <status,progress>=<{},{}>".format(self.order, self.status, self.progress )
