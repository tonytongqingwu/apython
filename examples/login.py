import os
import sys
import time
from apython.apps.app import AppiumApps, G7_APP


id_adb = sys.argv[1]
appium_d = AppiumApps(id_adb)
"""
This is part of script that you need check alert at any moment.
"""
appium_d.run_app(G7_APP)
appium_d.g7_login('tst1.andr.us@gmail.com', 'Test1ng2022')
