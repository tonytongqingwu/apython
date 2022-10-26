import random
import os
from time import sleep
from datetime import datetime
from apython.utils import get_wip_id, create_log_path, remove_appium
from apython.apps.app import *
from apython.grpc.gclient import GrpcClient
from apython.utils import get_transmitter_info, log_info, record_apps, logcat


if __name__ == '__main__':
    app_d = AppiumApps('014AY1RRR3')
    # app_d.verify_and_ack_alert('dexcomone')
    if app_d.g7_verify_signal_loss_message('dexcomone'):
        print('has message')

    # if app_d.g7_verify_signal_loss_alert():
    #     app_d.g7_click_ok_alert_ack()
    # elif app_d.g7_verify_signal_loss_message():
    #     print('loss')
    # else:
    #     egv = g.get_egv()
    #     print(egv)
    #     m_egv = app_d.get_egv()
    #     print(m_egv)
    #
    #     if str(egv) == m_egv:
    #         print('Pass: match')
    #     else:
    #         print('Fail: EGV not match: transmitter>{}, {}<mobile'.format(egv, m_egv))
    #
    #     if m_egv == '':
    #         print('Fail: G7 app has no EGV !!!')
    #
    #     print('Click ack OK button if any other alert')
    #     app_d.g7_click_ok_alert_ack()
