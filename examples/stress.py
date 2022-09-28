import sys
import random
import time
import os
from apython.apps.app import *


def record_top(file_name, value):
    with open(file_name, 'w') as f:
        f.writelines(str(value))


def record_apps(file_name, value):
    with open(file_name, 'a') as f:
        f.write(value + ',')


if __name__ == '__main__':
    """
    adb id must be provided
    """
    id_adb = sys.argv[1]
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

    # app_d.run_app(CAMERA)
    while True:
        app_d.run_app(MUSIC)  # always run music
        record_apps(app_log, MUSIC)

        # can create own sequence of apps
        for app in APPS:
            app_d.run_app(app)
            record_apps(app_log, app)

        print('Run app randomly')
        app = random.choice(APPS)
        app_d.run_app(app)
        record_apps(app_log, app)

        app_d.run_app(MUSIC)  # always run music
        record_apps(app_log, MUSIC)

        m, c = app_d.get_top_info()
        if m < min_mem_free:
            min_mem_free = m
            record_top(top_mem, min_mem_free)

        if c > max_cpu_used:
            max_cpu_used = c
            record_top(top_cpu, max_cpu_used)

        app_d.run_app(G7_APP)
        record_apps(app_log, G7_APP)

        if app_d.g7_verify_signal_loss_alert():
            print("\033[91mSignal lost alert !!!\033[0m")
            app_d.save_screen('{}/signal_loss_alert'.format(log_path))
        elif app_d.g7_verify_signal_loss_message():
            print("\033[91mSignal loss message !!!\033[0m")
            app_d.save_screen('{}/signal_loss_message'.format(log_path))
        else:
            print('Click ack OK button')
            app_d.g7_click_ok_alert_ack()
