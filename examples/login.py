import os
import sys
import time
from apython.apps.app import AppiumApps, G7_APP
from apython.utils import remove_appium


id_adb = sys.argv[1]
appium_d = AppiumApps(id_adb)
"""
Make sure appium is running, if not, run:
appium --relaxed-security --command-timeout 120000
This is part of script that you need check alert at any moment.
"""
# remove_appium(id_adb)
appium_d.run_app(G7_APP)
appium_d.g7_login('tst1.andr.us@gmail.com', 'Test1ng2022')
# appium_d.g7_re_login('tst1.andr.us@gmail.com', 'Test1ng2022')
# appium_d.g7_login_later()
