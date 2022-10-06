import os
import time
from time import sleep
from apython.adbd import AdbDevice
from apython.utils import record_top, get_wip_id
from apython.apps.app import *


USB_PWR_OFF = 'python3 /Users/tt0622/Sandbox/G7X_Tests/src/test/resources/gx_utility_scripts/controlBoard.py usbpwr1 '

if __name__ == '__main__':
    id_adb = get_wip_id()
    print(id_adb)

    adb_d = AdbDevice(id_adb)
    print('wip is:')
    print(id_adb)

    model = adb_d.adb_get_model()
    print('----{}-----'.format(model))
    log_path = os.getenv('HOME')
    log_path = '{}/{}'.format(log_path, model)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, id_adb)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, time.strftime("%Y%m%d-%H%M%S"))
    os.system('mkdir {}'.format(log_path))

    min_mem_free = 4000
    max_cpu_used = 0

    top_mem = log_path + '/free_mem.log'
    top_cpu = log_path + '/used_cpu.log'

    # 1. Must turn off USB:
    os.system(USB_PWR_OFF + ' on')

    # app_d.run_app(CAMERA)
    while True:
        sleep(60)
        # get top info
        m, c = adb_d.adb_get_top_info()
        if m < min_mem_free:
            min_mem_free = m
            record_top(top_mem, min_mem_free)

        if c > max_cpu_used:
            max_cpu_used = c
            record_top(top_cpu, max_cpu_used)

        # 2. check battery
        if adb_d.adb_get_battery_level() < 8:
            print('Less than level 8 for battery, charging now')
            os.system(USB_PWR_OFF + ' off')
        elif adb_d.adb_get_battery_level() > 98:
            print('Over 98, cut the power now')
            os.system(USB_PWR_OFF + ' on')
        else:
            print('battery is ok now')
