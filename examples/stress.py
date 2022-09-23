import sys
from time import sleep
from apython.appm import AppiumDevice
from apython.adbd import AdbDevice
from apython.apps.apps import AppiumApps


def check_signal_loss(appium_d):
    has_loss = False
    try:
        if appium_d.verify_signal_loss_alert():
            print('Has alert')
            has_loss = True
        else:
            print('No alert')
    except Exception as e:
        print(e)
    finally:
        print('find no alert')

    try:
        if appium_d.verify_signal_loss_message():
            print('Has message')
            has_loss = True
        else:
            print('No message')
    except Exception as e:
        print(e)
    finally:
        print('Find no message')

    return has_loss


def record_top(file_name, value):
    with open(file_name, 'w') as f:
        f.writelines(str(value))


if __name__ == '__main__':
    """
    adb id and file path like '/Users/tt0622/Test/' is the folder, and 'Map' is prefix.
    python stress.py 989AY13LAL '/Users/tt0622/Test/Map'
    """
    id_adb = sys.argv[1]
    file_path = sys.argv[2]
    print(id_adb)
    app_d = AppiumApps(id_adb)
    min_mem_free = 4000
    max_cpu_used = 0

    print(app_d.driver.capabilities['deviceModel'])
    top_mem = file_path + '_free_mem.log'
    top_cpu = file_path + '_used_cpu.log'

    while True:
        app_d.run_apps()
        m, c = app_d.get_top_info()
        if m < min_mem_free:
            min_mem_free = m
            record_top(top_mem, min_mem_free)

        if c > max_cpu_used:
            max_cpu_used = c
            record_top(top_cpu, max_cpu_used)

        if check_signal_loss(app_d):
            print("\033[91mSignal lost !!!\033[0m")
            app_d.save_screen(file_path)




