import random
import time
import os
from apython.utils import get_id
from apython.adbd import AdbDevice
from apython.apps.app import *


def record_top(file_name, value):
    with open(file_name, 'w') as f:
        f.writelines(str(value))


def record_apps(file_name, value):
    with open(file_name, 'a') as f:
        f.write(value + ',')


if __name__ == '__main__':
    os.system('bash appium_start.sh')
    id_adb = get_id()
    print('id: ---------')
    print(id_adb)
    adb_d = AdbDevice(id_adb)
    wip = adb_d.set_adb_wifi()
    id_adb = wip + ':5555'
    app_d = AppiumApps(id_adb)

    # start top, battery check
    os.system('bash ./top_battery_check.sh')
    module = app_d.get_module()
    log_path = os.getenv('HOME')
    log_path = '{}/{}'.format(log_path, module)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, id_adb)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, time.strftime("%Y%m%d-%H%M%S"))
    os.system('mkdir {}'.format(log_path))

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
