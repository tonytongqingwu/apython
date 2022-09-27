import sys
from apython.appm import AppiumDevice


id_adb = sys.argv[1]
port = sys.argv[2]
appium_d = AppiumDevice(id_adb)

appium_d.set_adb_wifi(port)