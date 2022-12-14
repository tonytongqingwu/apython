from apython.appm import AppiumDevice
from apython.apps.map import Map
from apython.apps.music import Music
from apython.apps.g7 import G7
from apython.apps.g1 import G1
from apython.apps.g6 import G6
from apython.apps.settings import Settings
from apython.apps.browser import Chrome
from apython.apps.memory import MemoryFill
from apython.apps.camera import Camera

CAMERA = 'Camera'
MAP = 'Map'
CHROME = 'Chrome'
G7_APP = 'G7'
MUSIC = 'Music'
SETTINGS = 'Settings'
MEMORY = 'Memory'
G1_APP = 'G1'
G6_APP = 'G6'

APPS = [CAMERA, MAP, CHROME, G7_APP, MEMORY, SETTINGS, MUSIC]


class AppiumApps(AppiumDevice):
    def __init__(self, adb_id, port_num='4723', dexcom_app_type='G7'):
        super().__init__(adb_id, port_num=port_num, dexcom_app_type=dexcom_app_type)

    def run_app(self, app):
        if app == MUSIC:
            Music.appium_youtube_music(self, 30)
        elif app == MAP:
            Map.navigate(self)
        elif app == G7_APP:
            G7.launch_g7(self)
        elif app == G1_APP:
            G1.launch_g1(self)
        elif app == G6_APP:
            G6.launch_g6(self)
        elif app == CAMERA:
            Camera.take_pictures(self)
        elif app == CHROME:
            Chrome.browse(self)
        elif app == SETTINGS:
            Settings.open_settings(self)
        elif app == MEMORY:
            MemoryFill.fill_memory(self)
