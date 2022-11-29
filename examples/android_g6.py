import random
import os
from time import sleep
from datetime import datetime
from apython.utils import get_wip_id, create_log_path, remove_appium
from apython.apps.app import *
# from apython.grpc.d1pake import D1Pake
# from apython.utils import get_transmitter_info_d1_pake, log_info, record_apps, logcat, get_id, compare_egv
from apython.utils import record_apps,  get_id, logcat, log_info


if __name__ == '__main__':
    id_adb = get_id()
    print('wip is:')
    print(id_adb)
    if id_adb == '' or id_adb is None:
        print('No id , exit !!!')
        print('you can kill battery script now')
        exit(1)

    app_d = AppiumApps(id_adb)
    app_d.run_app(G6_APP)
