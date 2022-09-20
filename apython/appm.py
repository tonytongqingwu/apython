import os
import sys
import subprocess
import datetime
import base64
import re
from time import sleep
from appium import webdriver
from datetime import datetime
from appium.webdriver.common.touch_action import TouchAction
from apython.adbd import AdbDevice


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
        print(self.common_desired_cap)
        print("appium server port number :", self.port_num)
        self.driver = webdriver.Remote("http://localhost:" + self.port_num + "/wd/hub", self.common_desired_cap)
        self.driver.update_settings({
            "waitForIdleTimeout": 3000,  # 3 seconds
        })

    def appium_touch_move_down(self):
        try:
            touch = TouchAction(self.driver)
            touch.long_press(x=500, y=550).move_to(x=500, y=1300).release().perform()
            sleep(3)
        except Exception as e:
            print(e)
            print("Unable to Scroll up to down")

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

    def appium_set_volume_percentages(self, pct_list):
        """
        Set all percentages for Ringtone, Media, Notification and System
        :param pct_list: list of percentages value of above
        :return: None
        """
        # todo: not working:
        # self.driver.start_activity('com.android.settings', 'QuickSettingsTile')
        self.appium_tap_title_contains('Sounds')
        self.appium_tap_title_contains('Volume')
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


appium_d = AppiumDevice('573052324e573398', '4723', 'G7')
appium_d.driver.keyevent(3)
adb_d = AdbDevice('573052324e573398')
adb_d.start_app_settings()
# appium_d.driver.save_screenshot('appium.png')
appium_d.appium_set_volume_percentages([68, 58, 48, 38])
# appium_d.stop()

