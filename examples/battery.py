import os
import os.path
from time import sleep
from apython.adbd import AdbDevice
from apython.utils import record_top, get_id, create_log_path


board_control_file = os.getenv('HOME') + '/Sandbox/G7X_Tests/src/test/resources/gx_utility_scripts/controlBoard.py'
USB_PWR_OFF = 'python3 ' + board_control_file + ' usbpwr1 '
BATTERY_LOW = 4   # when level low than this, start charging, 2 is not working
BATTERY_HIGH = 18  # when level high than this, stop charging

if __name__ == '__main__':
    if os.path.isfile(board_control_file):
        has_board = True
    else:
        has_board = False

    # set wip, must turn on power to get adb back
    if has_board:
        os.system(USB_PWR_OFF + ' off')
    sleep(10)
    id_adb = get_id()
    print('id: ---------')
    print(id_adb)

    if id_adb == '':
        print('Device must have no power, gives sometime to charge a bit')
        sleep(30)
        exit(1)

    adb_d = AdbDevice(id_adb)
    wip = adb_d.set_adb_wifi()
    id_adb = wip + ':5555'

    if wip:
        if has_board:
            os.system(USB_PWR_OFF + ' on')
        print('Got wip')
    else:
        print('No wifi is setup , exit !!!')
        exit(1)

    adb_d = AdbDevice(id_adb)
    print('wip is:')
    print(id_adb)

    # create folder
    model = adb_d.adb_get_model()
    print('----{}-----'.format(model))
    log_path = create_log_path(model, id_adb)
    print('log path {}'.format(log_path))

    min_mem_free = 4000
    max_cpu_used = 0

    top_mem = log_path + '/free_mem.log'
    top_cpu = log_path + '/used_cpu.log'

    while True:
        # check battery
        if has_board:
            if adb_d.adb_get_battery_level() < BATTERY_LOW:
                print('Less than level 8 for battery, charging now')
                os.system(USB_PWR_OFF + ' off')
            elif adb_d.adb_get_battery_level() > BATTERY_HIGH:
                print('Over 18, cut the power now')
                os.system(USB_PWR_OFF + ' on')

        # never charge until battery dies, and adb got lost connection
        # 98 battery can run a while
        # if adb_d.adb_get_battery_level() > 98:
        #     print('Over 98, cut the power now')
        #     os.system(USB_PWR_OFF + ' on')
        # else:
        #     print('battery is ok now')

        sleep(60)
        # get top info
        m, c = adb_d.adb_get_top_info()
        if m < min_mem_free:
            min_mem_free = m
            record_top(top_mem, min_mem_free)

        if c > max_cpu_used:
            max_cpu_used = c
            record_top(top_cpu, max_cpu_used)
