from time import sleep
from apython.appm import AppiumDevice
from apython.utils import run_command


class Map(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def navigate(self):
        print('Run Google Map')
        try:
            if 'SM-F721U' in self.driver.capabilities['deviceModel']:
                run_command('adb -s {} shell am start -n com.google.android.apps.maps/com.google.android.maps.MapsActivity'.format(self.adb_id))
            elif 'T55' in self.driver.capabilities['deviceModel']:
                run_command('adb -s {} shell monkey -p com.google.android.apps.mapslite -c android.intent.category.LAUNCHER 1'.format(self.adb_id))
            else:
                self.driver.start_activity('com.google.android.apps.maps', 'com.google.android.maps.MapsActivity')
            sleep(4)
            print("Navigating Up and Down")
            self.appium_touch_move_up()
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_down()
            self.appium_touch_move_down()
            self.back(3)
            print("Exit: GoogleMaps")
            print("____________________________________________________________________\n")
            self.back(5)
        except Exception as e:
            print(str(e))
            print(type(e))
            self.back(5)
            if "A session is either terminated or not started" in str(e):
                self.server_error_recovery()
            if "An unknown server-side error" in str(e):
                self.driver.quit()
                sleep(2)
                self.server_error_recovery()
        finally:
            print('Done map')
            self.back(5)
            self.home()


