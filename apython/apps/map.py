from time import sleep
from apython.appm import AppiumDevice


class Map(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def navigate(self):
        print('Run Google Map')
        self.driver.start_activity('com.google.android.apps.maps', 'com.google.android.maps.MapsActivity')
        sleep(4)
        try:
            # Click on 1st tab
            print("Click on First Tab")
            # self.driver.find_element_by_xpath("//android.widget.Button[@index='0']").click()
            # sleep(2)
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


