import sys
import random
import time
import os
from apython.apps.app import *
from apython.utils import record_top, get_app_list


"""
Example: Use apps.log as input to rerun 
input:   adb id
         file path
"""


if __name__ == '__main__':
    """
    adb id must be provided
    """
    id_adb = sys.argv[1]
    apps_file = sys.argv[2]
    print(id_adb)
    app_d = AppiumApps(id_adb)

    module = app_d.get_module()
    log_path = os.getenv('HOME')
    log_path = '{}/{}'.format(log_path, module)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, id_adb)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, time.strftime("%Y%m%d-%H%M%S"))
    os.system('mkdir {}'.format(log_path))

    min_mem_free = 4000
    max_cpu_used = 0

    print(app_d.driver.capabilities['deviceModel'])
    top_mem = log_path + '/free_mem.log'
    top_cpu = log_path + '/used_cpu.log'
    app_log = log_path + '/apps.log'

    apps_list = get_app_list(apps_file)
    for app in apps_list:
        app_d.run_app(app)  # always run music

        m, c = app_d.get_top_info()
        if m < min_mem_free:
            min_mem_free = m
            record_top(top_mem, min_mem_free)

        if c > max_cpu_used:
            max_cpu_used = c
            record_top(top_cpu, max_cpu_used)

