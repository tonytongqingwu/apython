import os
import sys
import time
from apython.apps.app import AppiumApps, G7_APP


id_adb = sys.argv[1]
appium_d = AppiumApps(id_adb)
module = appium_d.get_module()
log_path = os.getenv('HOME')
log_path = '{}/{}'.format(log_path, module)
os.system('mkdir {}'.format(log_path))
log_path = '{}/{}'.format(log_path, id_adb)
os.system('mkdir {}'.format(log_path))
log_path = '{}/{}'.format(log_path, time.strftime("%Y%m%d-%H%M%S"))
os.system('mkdir {}'.format(log_path))


"""
This is part of script that you need check alert at any moment.
"""

appium_d.run_app(G7_APP)
appium_d.g7_login('tst1.andr.us@gmail.com', 'Test1ng2022')
