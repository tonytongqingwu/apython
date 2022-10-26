import os
import sys
import datetime
import base64
import re
import time
from time import sleep
from appium import webdriver
from datetime import datetime
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from apython.utils import get_battery_level, get_top_info, remove_appium


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
        try:
            self.driver.stop_client()
        except Exception as e:
            print(e)

    def __init__(self, adb_id, port_num='4723', dexcom_app_type='G7'):
        self.adb_id = adb_id
        self.port_num = port_num
        self.dexcom_app_type = dexcom_app_type
        # Common desired capibilties and driver creation
        self.common_desired_cap = {
            "platformName": "Android",
            "udid": self.adb_id,
            "automationName": "UiAutomator2",
            "adbExecTimeout": 190000,
            "appWaitDuration": 190000,
            "uiautomator2ServerLaunchTimeout": 190000,
            "uiautomator2ServerInstallTimeout": 190000,
            "androidInstallTimeout": 180000,
            "disableWindowAnimation": True
        }
        # print(self.common_desired_cap)
        # print("appium server port number :", self.port_num)
        try:
            # self.server_error_recovery()
            self.driver = webdriver.Remote("http://localhost:" + self.port_num + "/wd/hub", self.common_desired_cap)
        except Exception as e:
            print(e)
            if 'HTTPConnection' in str(e):
                print('------------------------------------------------------------------')
                print('You need run "appium --relaxed-security" from other terminal first !')
                print('------------------------------------------------------------------')
                exit(1)

        self.driver.update_settings({
            "waitForIdleTimeout": 3000,  # 3 seconds
        })
        print('done init')

    def adb_get_battery_level(self):
        result = self.driver.execute_script('mobile: shell', {
            'command': 'dumpsys battery',
            'args': ['battery', '|', 'grep', 'level'],
            'includeStderr': True,
            'timeout': 5000
        })

        out = result['stdout']
        print(out)
        return get_battery_level(out)

    def get_top_info(self):
        result = self.driver.execute_script('mobile: shell', {
            'command': 'top',
            'args': ['-n', '1', '|', 'head', '-4'],
            'includeStderr': True,
            'timeout': 5000
        })

        return get_top_info(result['stdout'])

    def server_error_recovery(self):
        print("Server Error Recovery .... .. .... ......")
        remove_appium(self.adb_id)
        self.driver = webdriver.Remote("http://localhost:" + self.port_num + "/wd/hub", self.common_desired_cap)

    def adb_open_url(self, url):
        os.system("adb -s " + self.adb_id +
                  " shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d " + url)

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

    def get_model(self):
        m = self.driver.capabilities['deviceModel']
        m = m.replace(' ', '')
        return m

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
            print("Unable to scroll down")

    def g7_login_later(self):
        try:
            self.driver.find_element_by_id('com.dexcom.g7:id/id_login_later_button').click()
        except Exception as e:
            print('Login screen failed ' + str(e))

    def g7_re_login(self, user_nm, pass_wd):
        try:
            self.driver.find_element_by_id('com.dexcom.g7:id/id_login_now_button').click()
            sleep(30)
            self.driver.find_element_by_id('login_id_btn').click()
            # username = self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='username']")
            # username.click()
            # username.send_keys(user_nm)
            # # self.driver.keyevent(61)
            # passwd = self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='password']")
            # passwd.send_keys(pass_wd)
            # self.driver.keyevent(66)
            # sleep(60)
            # self.driver.find_element_by_xpath("(//android.widget.CheckBox)[1]").click()
            # self.driver.find_element_by_xpath("(//android.widget.CheckBox)[2]").click()
        except Exception as e:
            print('Login failed ' + str(e))

    def g7_login(self, user_nm, pass_wd):
        try:
            self.driver.find_element_by_id('com.dexcom.g7:id/id_login_button').click()
            sleep(30)
            username = self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='username']")
            username.click()
            username.send_keys(user_nm)
            # self.driver.keyevent(61)
            passwd = self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='password']")
            passwd.send_keys(pass_wd)
            self.driver.keyevent(66)
            sleep(60)
            self.driver.find_element_by_xpath("(//android.widget.CheckBox)[1]").click()
            self.driver.find_element_by_xpath("(//android.widget.CheckBox)[2]").click()
        except Exception as e:
            print('Login failed ' + str(e))

        try:
            username = self.driver.find_element_by_id('mat-input-0')
            username.click()
            username.send_keys(user_nm)
        except Exception as e:
            print('Different login failed ' + str(e))

    def get_egv(self, app='g7'):
        egv = ''
        try:
            egv = self.driver.find_element_by_id('com.dexcom.{}:id/id_glucose_compass_egv'.format(app)).text
        except NoSuchElementException as e:
            print('No EGV ' + str(e))
        finally:
            return egv

    def verify_and_ack_alert(self, app='g7'):
        ok = None
        try:
            ok = self.driver.find_element_by_id('com.dexcom.{}:id/id_alert_acknowledge_button'.format(app))
        except NoSuchElementException as e:
            print('No Alert ok' + str(e))
        finally:
            if ok:
                ok.click()
                return True
            else:
                return False

    def g7_verify_signal_loss_message(self, app='g7'):
        """
        Verify signal loss after 10 minutes with message
        :return:
        """
        lost_help = lost_title = None
        try:
            lost_help = self.driver.find_element_by_id('com.dexcom.{}:id/id_glucose_state_card_help_button'.format(app))
        except NoSuchElementException as e:
            print('Get lost_help button failed ' + str(e))

        try:
            lost_title = self.driver.find_element_by_id('com.dexcom.{}:id/id_glucose_state_card_title_label'.format(app))
        except NoSuchElementException as e:
            print('Get lost_title  failed ' + str(e))

        if lost_help and lost_title and lost_title.text == 'Signal Loss':
            return True
        else:
            return False

    def g7_click_ok_alert_ack(self):
        try:
            self.driver.find_element_by_id('com.dexcom.g7:id/id_alert_acknowledge_button').click()
        except Exception as e:
            print('Clike ack alert failed ' + str(e))

        try:
            self.driver.find_element_by_id('com.dexcom.g7:id/snackbar_action').click()
        except Exception as e:
            print('Click bar failed ' + str(e))

    def g7_verify_signal_loss_alert(self, app='g7'):
        """
        Verify signal loss after 20 minutes with message
        :return:
        """
        lost_ok = lost_title = None
        try:
            lost_ok = self.driver.find_element_by_id('com.dexcom.{}:id/id_alert_acknowledge_button'.format(app))
        except NoSuchElementException as e:
            print('Get lost_ok button failed ' + str(e))

        try:
            lost_title = self.driver.find_element_by_id('com.dexcom.{}:id/id_alert_title_label'.format(app))
        except NoSuchElementException as e:
            print('Get lost_title  failed ' + str(e))

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
            print("Unable to scroll up")

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
            print(type(bounds))
            start_x, start_y, end_x, end_y = get_bar_move_by_pct(bounds, pct_list[i])
            try:
                touch = TouchAction(self.driver)
                touch.long_press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release().perform()
                sleep(1)
            except Exception as e:
                print(e)
                print("Unable to move the bar")
            finally:
                print('Done bar moving')
