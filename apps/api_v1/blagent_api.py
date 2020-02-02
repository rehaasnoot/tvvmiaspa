import requests
import os
import urllib3
import tarfile
import logging
import tempfile
import shutil
import time
import json
from ..settings import PROJECT_NAME, config, CONFIG_SECTION_NAME
from apps.tvvlogger import TVVLogger

LOG = TVVLogger(__name__)

class ApiError(Exception):  # An API Error Exception
    def __init__(self, status):
        self.status = status
    def __str__(self):
        return "APIError: status={}".format(self.status)

class TVVBlagent():
    name = 'Blender Agent'
    access_token = None
    refresh_token = None
    BLAGENT_PROTO = "http"
    BLAGENT_API_NAME = 'tvvblagent'
    BLAGENT_ID = None
    BLAGENT_HOST = None
    BLAGENT_PORT = None
    BLAGENT_USERNAME = config.get(CONFIG_SECTION_NAME, 'BLAGENT_USERNAME')
    BLAGENT_PASSWORD = config.get(CONFIG_SECTION_NAME, 'BLAGENT_PASSWORD')
    REGISTRY_HOST = 'localhost'
    REGISTRY_PORT = '6363'
    REGISTRY_USERNAME = config.get(CONFIG_SECTION_NAME, 'REGISTRY_USERNAME')
    REGISTRY_PASSWORD = config.get(CONFIG_SECTION_NAME, 'REGISTRY_PASSWORD')
    REGISTRY_API_NAME = 'tvvblagent_registry'
    BLAGENT_PACKAGE = None
    BLENDER_VERSION = None
    
    def blagentURI(self):
        uri = "{}://{}:{}/{}/".format(self.BLAGENT_PROTO, self.getHost(), self.getPort(), self.BLAGENT_API_NAME)
        return uri
    def getId(self):
        if None == self.BLAGENT_ID:
            self.lookup()
        return self.BLAGENT_ID
    def setId(self, id):
        self.BLAGENT_ID = id
    def getAccessToken(self):
        return self.access_token
    def setAccessToken(self, token):
        self.access_token = token
    def getRefreshToken(self):
        return self.refresh_token
    def setRefreshToken(self, token):
        self.refresh_token = token
    def getAuthToken(self):
        authCredentials = {'Authorization' : 'Bearer ' + self.getAccessToken() }
        return authCredentials
    def getAuthCredentials(self):
        basicCredentials = (self.REGISTRY_USERNAME, self.REGISTRY_PASSWORD) 
        return basicCredentials
    def getHost(self):
        if None == self.BLAGENT_HOST:
            self.lookup()
        return self.BLAGENT_HOST
    def setHost(self, host):
        self.BLAGENT_HOST = host
    def getPort(self):
        if None == self.BLAGENT_PORT:
            self.lookup()
        return self.BLAGENT_PORT
    def setPort(self, port):
        self.BLAGENT_PORT = port
    def getAgentUrl(self, functionName):
        api_agent_url = "{}://{}:{}/{}/{}".format(self.BLAGENT_PROTO, self.getHost(), self.getPort(), self.BLAGENT_API_NAME, functionName)
        return api_agent_url
    def getReqUrl(self, functionName):
        api_req_url = 'http://{}:{}/{}/{}'.format(self.REGISTRY_HOST, self.REGISTRY_PORT, self.REGISTRY_API_NAME, functionName)
        return api_req_url
    def login(self):
        api_req_url = self.getReqUrl('login')
        resp = None
        while None == resp or resp.status_code != 200:
            resp = requests.post(api_req_url, auth=self.getAuthCredentials())
            time.sleep(2)
        resp_json = json.loads(resp.text)
        self.setAccessToken(resp_json["access_token"])
        self.setRefreshToken(resp_json['refresh_token'])
        return True
    def lookup(self):
        api_req_url = api_req_url = self.getReqUrl('lookup')
        resp = None
        while None == resp or resp.status_code not in (200, 201):
            if None == self.getAccessToken():
                self.login()
            resp = requests.get(api_req_url, headers=self.getAuthToken())
            if resp.status_code == 401:
                self.setAccessToken(None)
            time.sleep(4)
        if resp.status_code == 200:
            resp_json = json.loads(resp.text)
            self.setId(resp_json["id"])
            self.setHost(resp_json["host"])
            self.setPort(resp_json["port"])
            self.setAccessToken(resp_json["access_token"])
            self.setRefreshToken(resp_json['refresh_token'])
            return True
        return false
    def getMidiTrackList(self, midi_file_name):
        self.lookup()
        api_req_url = self.getAgentUrl('miditracks')
        f = open(midi_file_name, 'rb')
        r = requests.get(api_req_url, files={'midi_file' : f} )
        status_code = r.status_code
        f.close()
    def make_pkg(self, blend_file, instrument_file, midi_file):
        torf = None
        id = self.getId()
        if None == id:
            self.lookup()
            id = self.getId()
        staging_path = os.path.join('/', 'tmp', id)
        temp_name = id
        temp_tar = os.path.join(staging_path, temp_name) + '.b2z'
        temp_blend = os.path.join(staging_path, temp_name + '.p.blend')
        temp_midi = os.path.join(staging_path, temp_name + '.midi')
        temp_inst_blend = os.path.join(staging_path, temp_name + '.i.blend')
        temp_inst = os.path.join(staging_path, temp_name + '.blend')
        if not os.path.isdir(staging_path):
            try:
                os.mkdir(staging_path)
            except OSError:
                print ("Creation of the directory %s failed" % staging_path)
                return False
            else:
                print ("Successfully created the directory %s " % staging_path)
        with tarfile.open(temp_tar, 'w:bz2') as package:
            shutil.copyfile(blend_file, temp_blend)
            package.add(temp_blend, arcname=temp_name + '.p.blend')
            shutil.copyfile(midi_file, temp_midi)            
            package.add(temp_midi, arcname=temp_name + '.midi')
            shutil.copyfile(instrument_file, temp_inst_blend)  
            package.add(temp_inst_blend, arcname=temp_name + '.i.blend')
            package.close()
        f = open(temp_tar, 'rb')
        return f
    def assemble(self, fps, track_ids, player_name, instrument_name, blend_file, instrument_file, class_name, midi_file, frame_start, frame_end):
        self.lookup()
        torf = False
        ctrl_data = { "fps" : fps,
                      "frame_start" : frame_start,
                      "frame_end" : frame_end,
                      "track_ids": track_ids,
                      "player_name": player_name,
                      "instrument_name": instrument_name,
                      "instrument_class": class_name
                    }
        f = self.make_pkg(blend_file, instrument_file, midi_file)
        payload = ctrl_data
        files = {'blagent_package': f}
        authCredentials = {'Authorization' : 'Bearer ' + self.getAccessToken() }
        resp = requests.request(method='POST', url=self.getAgentUrl('assemble'), headers=authCredentials,
                files=files, data=payload)
        status_code = resp.status_code
        LOG.log("<status_code>=<{}>".format(status_code))
        if status_code < 205:
            torf = True
        return torf
            
    def transmit_and_assemble(self, blend_file, instrument_file, midi_file):
        assemble_id = self.transmit(blend_file, instrument_file, midi_file)
        if None != assemble_id:
            self.assemble(assemble_id, track_id, player_name, instrument_name)
        
