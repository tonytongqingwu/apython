import sys
from apython.appm import AppiumDevice
from apython.adbd import AdbDevice


def music(appium_d):
    appium_d.appium_youtube_music(10)
    # appium_d.save_screen('/Users/tt0622/music')
    # adb_d.dump_top_cpu('/Users/tt0622/music')


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


if __name__ == '__main__':
    id_adb = sys.argv[1]
    file_path = sys.argv[2]
    print(id_adb)
    app_d = AppiumDevice(id_adb, '4723', 'G7')
    print(app_d.driver.capabilities['deviceModel'])
    adb_d = AdbDevice(id_adb)
    while True:
        music(app_d)
        app_d.launch_blue_g7()
        if check_signal_loss(app_d):
            app_d.save_screen(file_path)
            adb_d.dump_top_cpu(file_path)


