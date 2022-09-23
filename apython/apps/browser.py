from time import sleep
from apython.appm import AppiumDevice


class Chrome(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def browse(self):
        print("-------------------------------------")
        print("Opening Chrome Browser")
        print("-------------------------------------")
        sleep(2)
        try:
            self.driver.get('www.Dexcom.com')
            print("Navigating Up and Down")
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_down()
            sleep(2)
            self.appium_touch_move_down()

            self.driver.get('www.google.com')
            self.driver.find_element_by_xpath(".//android.widget.EditText").send_keys('CGM')
            self.driver.find_element_by_xpath(".//android.widget.Button[@text='Google Search']").click()
            # Press Enter on Mobile keyboard
            self.enter()
            sleep(3)
            print("Navigating Up and Down")
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_down()
            sleep(2)
            self.appium_touch_move_down()
            # Click on Images Tab on Browser
            print("Click on Images Tab")
            self.driver.find_element_by_xpath(".//android.widget.TextView[@text='Images']").click()
            print("Navigating Up and Down")
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_up()
            sleep(2)
            self.appium_touch_move_down()
            sleep(2)
            self.appium_touch_move_down()
            # CLOSE ALL TABS
            print("Click Switcher Icon--More Options--Close All")
            self.driver.find_element_by_id("com.android.chrome:id/tab_switcher_button").click()
            sleep(2)
            self.driver.find_element_by_xpath("//android.widget.ImageButton[@content-desc='More options']").click()
            sleep(2)
            self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Close all tabs']").click()
            print("Closed all opened Tabs in Google Chrome")
            sleep(5)
            print("Exit: Chrome_Browser")
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
            print('Done Browser')
