import sys
from apython.appm import AppiumDevice
from apython.adbd import AdbDevice


def music(appium_d):
    appium_d.appium_youtube_music(10)
    # appium_d.save_screen('/Users/tt0622/music')
    # adb_d.dump_top_cpu('/Users/tt0622/music')


if __name__ == '__main__':
    id_adb = sys.argv[1]
    print(id_adb)
    app_d = AppiumDevice(id_adb, '4723', 'G7')
    print(app_d.driver.capabilities['deviceModel'])
    adb_d = AdbDevice(id_adb)
    music(app_d)


