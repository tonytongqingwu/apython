from time import sleep
from apython.appm import AppiumDevice


class Settings(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def open_settings(self):
        print("-------------------------------------")
        print("Open Settings on Mobile Device")
        print("-------------------------------------")
        sleep(2)
        try:
            print("Open Settings")
            self.driver.start_activity('com.android.settings')
            sleep(4)
            print("Navigating Up and Down")
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_down()
            sleep(1)
            print("Scroll Up and Down")
            print("Press Device Home Button")
            self.home()
            print("Exit: openSettings_on_Mobile")
            print("____________________________________________________________________\n")
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
            print('Done Settings')
