from apython.appm import AppiumDevice
from apython.apps.map import Map
from apython.apps.music import Music
from apython.apps.g7 import G7
from apython.apps.settings import Settings
from apython.apps.browser import Chrome
from apython.apps.memory import MemoryFill


class AppiumApps(AppiumDevice):
    def __init__(self, adb_id, port_num='4723', dexcom_app_type='G7'):
        super().__init__(adb_id, port_num=port_num, dexcom_app_type=dexcom_app_type)

    def run_apps(self):
        Music.appium_youtube_music(self, 100)
        Map.navigate(self)
        G7.launch_blue_g7(self)

    def run_any_app(self):
        print('Run app randomly')

