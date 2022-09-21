import os
import sys
import subprocess
import datetime
import base64
import re
import time
from time import sleep
from appium import webdriver
from datetime import datetime
from appium.webdriver.common.touch_action import TouchAction


def get_bar_move_by_pct(bounds, pct):
    m = re.search('^\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
    if m:
        start_x = int(m.group(1))
        start_y = int(m.group(2))
        end_x = int(m.group(3))
        end_y = int(m.group(4))

    pct_x = int((end_x - start_x) * pct / 100)
    return start_x, start_y, pct_x, end_y


class AppiumDevice:
    def __del__(self):
        self.driver.stop_client()
        # self.driver.close()

    def __init__(self, adb_id, port_num, dexcom_app_type):
        self.adb_id = adb_id
        self.port_num = port_num
        self.dexcom_app_type = dexcom_app_type
        # Common desired capibilties and driver creation
        self.common_desired_cap = {
            "platformName": "Android",
            "udid": self.adb_id,
            "automationName": "UiAutomator2",
            "adbExecTimeout": 60000,
            "appWaitDuration": 60000,
            "uiautomator2ServerLaunchTimeout": 90000,
            "uiautomator2ServerInstallTimeout": 60000,
            "androidInstallTimeout": 180000,
            "disableWindowAnimation": True
        }
        # print(self.common_desired_cap)
        # print("appium server port number :", self.port_num)
        self.driver = webdriver.Remote("http://localhost:" + self.port_num + "/wd/hub", self.common_desired_cap)
        self.driver.update_settings({
            "waitForIdleTimeout": 3000,  # 3 seconds
        })

    def appium_youtube_music(self, play_time):
        self.driver.activate_app('com.google.android.apps.youtube.music')
        sleep(3)
        try:
            print("Click on search icon")
            # self.driver.find_element_by_xpath(".//android.widget.ImageView[@content-desc='Search']").click()
            self.driver.find_element_by_id('com.google.android.apps.youtube.music:id/action_search_button').click()
            sleep(3)
            search_text = 'two hours soulful medidation'
            # edit = self.driver.find_element_by_id('com.google.android.apps.youtube.music:id/search_edit_text')
            edit = self.driver.find_element_by_xpath(".//android.widget.EditText").send_keys(search_text)
            if edit:
                print('find edit')
            edit.send_keys(search_text)

            self.enter()
            sleep(3)
            print("Scrolling Up and Down")
            self.appium_touch_move_up()
            sleep(1)
            self.appium_touch_move_up()
            sleep(1)
            self.appium_touch_move_down()
            sleep(1)
            print("Click on Video to Play")
            self.driver.find_element_by_xpath(".//android.view.ViewGroup[@index='0']").click()
            try:
                self.driver.find_element_by_id("com.google.android.youtube:id/skip_ad_button_container").click()
            except Exception as e:
                print("No ad")
            finally:
                print('Start music')

            sleep(play_time)
            sleep(3)
            print("Closing the Video")
            print("Exit: Youtube Music")
            print("____________________________________________________________________\n")
            self.back(10)
        except Exception as e:
            print('Music errors: ' + str(e))
        finally:
            print('Done music')
            self.home()

    def home(self, times=1):
        for i in range(times):
            self.driver.keyevent(3)
            sleep(0.1)

    def back(self, times=1):
        for i in range(times):
            self.driver.keyevent(4)
            sleep(0.1)

    def enter(self):
        self.driver.keyevent(66)

    def save_screen(self, name):
        """
        Save screen with id, timestamp
        :param name: full path name, ex. /Users/tt0622/screen_test
        :return: /Users/tt0622/screen_test_xxx_2022-021359.png
        """
        f_name = '{}_{}_{}.png'.format(name, self.adb_id, time.strftime("%Y%m%d-%H%M%S"))
        self.driver.save_screenshot(f_name)

    def appium_touch_move_down(self):
        try:
            touch = TouchAction(self.driver)
            touch.long_press(x=500, y=550).move_to(x=500, y=1300).release().perform()
            sleep(3)
        except Exception as e:
            print(e)
            print("Unable to Scroll up to down")
        finally:
            print('move down failed')

    def verify_signal_loss_message(self):
        """
        Verify signal loss after 10 minutes with message
        :return:
        """
        try:
            lost_help = self.driver.find_element_by_id('com.dexcom.g7:id/id_glucose_state_card_help_button')
        except Exception as e:
            print('Get lost_help button failed ' + e)

        try:
            lost_title = self.driver.find_element_by_id('com.dexcom.g7:id/id_glucose_state_card_title_label')
        except Exception as e:
            print('Get lost_title  failed ' + e)

        if lost_help and lost_title and lost_title.text == 'Signal Loss':
            return True
        else:
            return False

    def verify_signal_loss_alert(self):
        """
        Verify signal loss after 20 minutes with message
        :return:
        """
        try:
            lost_ok = self.driver.find_element_by_id('com.dexcom.g7:id/id_alert_acknowledge_button')
        except Exception as e:
            print('Get lost_ok button failed ' + e)

        try:
            lost_title = self.driver.find_element_by_id('com.dexcom.g7:id/id_alert_title_label')
        except Exception as e:
            print('Get lost_title  failed ' + e)

        if lost_ok and lost_title and lost_title.text == 'Signal Loss':
            return True
        else:
            return False

    def appium_tap_title_contains(self, text):
        titles = self.driver.find_elements_by_id('android:id/title')
        for t in titles:
            if text in t.text:
                t.click()
                sleep(2)
                break

    def appium_touch_move_up(self):
        try:
            touch = TouchAction(self.driver)
            touch.long_press(x=500, y=1300).move_to(x=500, y=550).release().perform()
            sleep(3)
        except Exception as e:
            print(e)
            print("Unable to Scroll down to up")
        finally:
            print('Move up failed')

    def appium_set_volume_percentages(self, pct_list):
        """
        Set all percentages for Ringtone, Media, Notification and System
        :param pct_list: list of percentages value of above
        :return: None
        """
        self.driver.activate_app('com.android.settings')
        self.appium_tap_title_contains('Sound')
        if 'Pixel' in self.driver.capabilities['deviceModel']:
            print('Pixel has no Volume menu')
        else:  # samsung SX has Volume menu
            self.appium_tap_title_contains('Volume')  # S9
        bars = self.driver.find_elements_by_id('android:id/seekbar')
        for i in range(4):
            bounds = bars[i].get_attribute('bounds')
            print(bounds)
            start_x, start_y, end_x, end_y = get_bar_move_by_pct(bounds, pct_list[i])
            try:
                touch = TouchAction(self.driver)
                touch.long_press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release().perform()
                sleep(1)
            except Exception as e:
                print(e)
                print("Unable to move the bar")
            finally:
                print('Bar moving failed')


