from django.test import TestCase
from uuid import uuid1
from random import random
from django.contrib.auth.models import User, Group
from apps.tvvroot.models import Music, Video, Player, Instrument, Order, Blender

SCALE = 1000
RAND = int(random() * SCALE)
TEST_UUID = uuid1(RAND)
TEST_TITLE = "test." + str(RAND)
TEST_NAME = 'name' + str(RAND)
TEST_DESCRIPTION = "description" + str(RAND)
TEST_GROUP_NAME = "testing"
TEST_USER_NAME = "testuser"

def rand():
    return int(random() * SCALE)
def randstr():
    return str(rand())

class TVVTestCase(TestCase):
    def _setUp(self, setupClass):
        setup = setupClass()
        setup.setUp()
        return setup

class TestGroup(TVVTestCase):
    TEST_GROUP = None
    def setUp(self):
        self.TEST_GROUP = Group.objects.create(name=TEST_GROUP_NAME + randstr())
    def test_group(self):
        testGroup = Group.objects.get(name=self.TEST_GROUP.name)
        self.assertEqual(testGroup.id, self.TEST_GROUP.id, self)

class TestUser(TVVTestCase):
    TEST_GROUP = None
    def setUp(self):
        self.TEST_GROUP = self._setUp(TestGroup).TEST_GROUP
        self.TEST_USER = User.objects.create(username=TEST_USER_NAME)
    def test_this(self):
        testUser = User.objects.get(username=TEST_USER_NAME)
        self.assertEqual(testUser.username, TEST_USER_NAME, self)
    
class TestMusic(TVVTestCase):
    TEST_MUSIC = None
    def setUp(self):
        Music.objects.create(uuid=uuid1(RAND), title=TEST_TITLE + 'a', midi=None, audio=None)
        self.TEST_MUSIC = Music.objects.create(uuid=TEST_UUID, title=TEST_TITLE, midi=None, audio=None)
    def test_this(self):
        testMusic = Music.objects.get(uuid=TEST_UUID)
        self.assertEqual(testMusic.title, TEST_TITLE, self)
        
class TestVideo(TVVTestCase):
    TEST_VIDEO = None
    def setUp(self):
        Video.objects.create(uuid=uuid1(RAND), title=TEST_TITLE + 'b', video=None)
        self.TEST_VIDEO = Video.objects.create(uuid=TEST_UUID, title=TEST_TITLE, video=None)
    def test_this(self):
        second = Video.objects.get(uuid=TEST_UUID)
        self.assertEqual(second.title, TEST_TITLE, self)
    
class TestPlayer(TVVTestCase):
    TEST_PLAYER = None
    def setUp(self):
        Player.objects.create(uuid=uuid1(RAND), name=TEST_NAME + TEST_DESCRIPTION, description=TEST_DESCRIPTION + TEST_NAME)
        self.TEST_PLAYER = Player.objects.create(uuid=TEST_UUID, name=TEST_NAME, description=TEST_DESCRIPTION)
    def test_this(self):
        second = Player.objects.get(uuid=TEST_UUID)
        self.assertEqual(second.name, TEST_NAME, self)
    
class TestInstrument(TVVTestCase):
    TEST_INSTRUMENT = None
    def setUp(self):
        Instrument.objects.create(uuid=uuid1(RAND), name=TEST_NAME + TEST_DESCRIPTION, description=TEST_DESCRIPTION +TEST_NAME)
        self.TEST_INSTRUMENT = Instrument.objects.create(uuid=TEST_UUID, name=TEST_NAME, description=TEST_DESCRIPTION)
    def test_instrument(self):
        second = Instrument.objects.get(id=self.TEST_INSTRUMENT.id)
        self.assertEqual(second.name, TEST_NAME, self)

class TestOrder(TVVTestCase):
    TEST_USER = None
    TEST_MUSIC = None
    TEST_PLAYER = None
    TEST_INSTRUMENT = None
    TEST_ORDER = None
    def setUp(self):
        self.TEST_USER = self._setUp(TestUser).TEST_USER
        self.TEST_MUSIC = self._setUp(TestMusic).TEST_MUSIC
        self.TEST_PLAYER = self._setUp(TestPlayer).TEST_PLAYER
        self.TEST_INSTRUMENT = self._setUp(TestInstrument).TEST_INSTRUMENT
        
    def test_this(self):
        self.TEST_ORDER = Order.objects.create(uuid=TEST_UUID, user_id=self.TEST_USER.id, player=self.TEST_PLAYER, music_pkg=self.TEST_MUSIC, instrument=self.TEST_INSTRUMENT)
        testOrder = Order.objects.get(id=self.TEST_ORDER.id)
        self.assertEqual(testOrder, self.TEST_ORDER, self)

