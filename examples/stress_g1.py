import random
import os
from time import sleep
from datetime import datetime
from apython.utils import get_wip_id, create_log_path, remove_appium
from apython.apps.app import *
from apython.grpc.d1pake import D1Pake
from apython.utils import get_transmitter_info_d1_pake, log_info, record_apps, logcat, get_id


G1_NAME = 'dexcomone'

if __name__ == '__main__':
    os.system('bash ./kill_ps.sh')
    # start top, battery check, create wip,
    os.system('bash ./top_battery_check_g1.sh')
    sleep(30)
    # power should cut already, so use wi-fi for appium
    # get wip
    id_adb = get_id()
    print('wip is:')
    print(id_adb)
    if id_adb == '' or id_adb is None:
        print('No id , exit !!!')
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
    info = log_path + '/info.log'

    prod_type, address, transmitter_id, pair_code = get_transmitter_info_d1_pake()
    g = D1Pake(address, transmitter_id)
    pause_time = None
    start_time = None
    pause_count = 0

    APPS = list(map(lambda x: x.replace(G1_APP, G1_APP), APPS))
    print(APPS)
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

        app_d.run_app(G1_APP)
        record_apps(app_log, G1_APP)

        now = datetime.now()
        if 0 < now.hour < 24:  # We can always make alert not sound by settings, so run 24 hours now.
            if pause_time is None:
                if start_time is None or (start_time is not None and (now - start_time).total_seconds() > 1800):
                    pause_time = now
                    pause_count += 1
                    msg = '{} - Pause {} times'.format(pause_time, pause_count)
                    print(msg)
                    log_info(info, msg)
                    g.save_state(2)
                    start_time = None
            else:
                print('has pause time already')
                if start_time is None and (now - pause_time).total_seconds() > 3000:
                    g.save_state(0)
                    start_time = now
                    msg = '{} - Start {} times'.format(start_time, pause_count)
                    print(msg)
                    log_info(info, msg)
                    pause_time = None
        else:
            print('Sleep time, make sure uncheck automatic mode on DrStrange.')

        msg = '{} Check G1'.format(datetime.now())
        log_info(info, msg)
        logcat(log_path, id_adb)
        if app_d.g7_verify_signal_loss_alert(app=G1_NAME):
            print("\033[91mSignal lost alert !!!\033[0m")
            msg = '{} Signal lost alert'.format(datetime.now())
            log_info(info, msg)
            # over 30 minute
            if pause_time is not None and (now - pause_time).total_seconds() > 2000:
                print('Fail: Alert is too late')
                log_info(info, '{} Fail: Alert is too late'.format(datetime.now()))
            if start_time is not None and (now - start_time).total_seconds() > 1900:
                print('Fail: Signal is not recovered')
                log_info(info, '{} Fail: Signal is not recovered on alert'.format(datetime.now()))
            app_d.save_screen('{}/signal_loss_alert'.format(log_path))
            app_d.g7_click_ok_alert_ack()
        elif app_d.g7_verify_signal_loss_message(app=G1_NAME):
            # over 16 minute
            if pause_time is not None and (now - pause_time).total_seconds() > 1100:
                print('Fail: Signal Lost Message is too late')
                log_info(info, '{} Fail: Signal is not recovered on message'.format(datetime.now()))
            if start_time is not None and (now - start_time).total_seconds() > 1900:
                print('Fail: Signal is not recovered - signal loss message still there')
                log_info(info, '{} Fail: Signal is not recovered'.format(datetime.now()))
            print("\033[91mSignal loss message !!!\033[0m")
            log_info(info, '{} Signal loss message'.format(datetime.now()))
            app_d.save_screen('{}/signal_loss_message'.format(log_path))
        else:
            egv = g.get_egv()
            print(egv)
            m_egv = app_d.get_egv(app=G1_NAME)
            print(m_egv)

            if str(egv) == m_egv:
                print('Pass: match')
            else:
                print('Fail: EGV not match: transmitter>{}, {}<mobile'.format(egv, m_egv))
                msg = '{} Fail: EGV not match: transmitter>{}, {}<mobile'.format(egv, m_egv, datetime.now())
                log_info(info, msg)

            if m_egv == '':
                print('Fail: G1 app has no EGV !!!')
                app_d.save_screen('{}/no_egv'.format(log_path))

            print('Click ack OK button if any other alert')
            app_d.g7_click_ok_alert_ack()
