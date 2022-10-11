import random
import os
from time import sleep
from datetime import datetime
from apython.utils import get_wip_id, create_log_path, remove_appium
from apython.apps.app import *
from apython.grpc.gclient import GrpcClient
from apython.utils import get_transmitter_info


def record_top(file_name, value):
    with open(file_name, 'w') as f:
        f.writelines(str(value))


def record_apps(file_name, value):
    with open(file_name, 'a') as f:
        f.write(value + ',')


if __name__ == '__main__':
    os.system('bash ./kill_ps.sh')
    # start top, battery check, create wip,
    os.system('bash ./top_battery_check.sh')
    sleep(20)
    # power should cut already, so use wi-fi for appium
    # get wip
    id_adb = get_wip_id()
    print('wip is:')
    print(id_adb)
    if id_adb == '' or id_adb is None:
        print('No wifi is setup , exit !!!')
        os.system('bash ./kill_ps.sh')
        exit(1)

    remove_appium(id_adb)

    os.system('bash appium_start.sh')
    sleep(20)

    app_d = AppiumApps(id_adb)

    model = app_d.get_model()
    log_path = create_log_path(model, id_adb)
    print('log path {}'.format(log_path))

    app_log = log_path + '/apps.log'

    prod_type, address, transmitter_id, pair_code = get_transmitter_info()
    g = GrpcClient(address, pair_code, transmitter_id)
    pause_time = None
    start_time = None

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

        now = datetime.now()
        if 8 < now.hour < 17:
            if not pause_time:
                pause_time = now
                print('Pause at {}'.format(pause_time))
                g.save_state('PAUSE_ADVERTISING')
            else:
                print('has pause time already')
                if (now - pause_time).total_seconds() > 3600:
                    g.save_state('START_ADVERTISING')
                    start_time = now
                    print('Start at {}'.format(start_time))

                    if start_time is not None:
                        if (now - start_time).total_seconds() > 2000:
                            g.save_state('PAUSE_ADVERTISING')
                            pause_time = now
        else:
            print('Sleep time, make sure uncheck automatic mode on DrStrange.')

            print("Test signal lost")
        if app_d.g7_verify_signal_loss_alert():
            print("\033[91mSignal lost alert !!!\033[0m")
            # over 30 minute
            if (now - pause_time).total_seconds() > 2000:
                print('Fail: Alert is too late')
                if start_time is not None:
                    if (now - start_time).total_seconds() > 1900:
                        print('Fail: Signal is not recovered')
            app_d.save_screen('{}/signal_loss_alert'.format(log_path))
            app_d.g7_click_ok_alert_ack()
        elif app_d.g7_verify_signal_loss_message():
            # over 16 minute
            if (now - pause_time).total_seconds() > 1100:
                print('Fail: Message is too late')
            if start_time is not None:
                if (now - start_time).total_seconds() > 1900:
                    print('Fail: Signal is not recovered - signal loss message still there')
            print("\033[91mSignal loss message !!!\033[0m")
            app_d.save_screen('{}/signal_loss_message'.format(log_path))
        else:
            egv = g.get_egv()
            print(egv)
            m_egv = app_d.get_egv()
            print(m_egv)

            if str(egv) == m_egv:
                print('match')
            else:
                print('EGV not match: transmitter>{}, {}<mobile'.format(egv, m_egv))

            print('Click ack OK button if any other alert')
            app_d.g7_click_ok_alert_ack()
