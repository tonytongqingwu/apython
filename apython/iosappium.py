import os
import sys
import datetime
import base64
import re
import time
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from apython.utils import get_battery_level, get_top_info, remove_appium

CAMERA = 'Camera'
MAP = 'Maps'
CHROME = 'Browser'
G7_APP = 'G7'
TV = 'TV'
SETTINGS = 'Settings'
MEMORY = 'Memory'

APPS = [CAMERA, MAP, CHROME, G7_APP, MEMORY, SETTINGS, TV]


class AppiumIOS:
    def __del__(self):
        try:
            self.driver.stop_client()
        except Exception as e:
            print(e)

    def __init__(self, device_id, port_num='4723', dexcom_app_type='G7'):
        self.device_id = device_id
        self.port_num = port_num
        self.dexcom_app_type = dexcom_app_type
        # Common desired capibilties and driver creation
        self.common_desired_cap = {
            "udid": self.device_id,
            "automationName": "XCUITest",
            # "wdaLocalPort": self.port_num,
            "autoAcceptAlerts": True,
            "platformName": "iOS",
            "deviceName": 'iPhone',
            # "xcodeOrgId": 'P762WHM474',
            "xcodeSigningId": 'iPhone Developer',
            "showIOSLog": True,
            "appium:noReset": True,
            "appium:autoAcceptAlerts": True,
            "newCommandTimeout": 600
        }
        try:
            self.driver = webdriver.Remote("http://0.0.0.0:" + self.port_num + "/wd/hub", self.common_desired_cap)
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
        self.touch = TouchAction(self.driver)
        print('done init')

    def open_settings(self):
        try:
            setting_icon = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "TV"))
            )
            setting_icon.click()
        except Exception as e:
            print('open setting failed')

        # input_search = WebDriverWait(self.driver, 20).until(
        #     EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "Search"))
        # )
        # input_search.send_key("Ab")

    def open_app(self, app_name):
        self.home()
        sleep(2)
        self.click_text(app_name)
        print('Open app {}'.format(app_name))

    def run_app(self, app_name):
        self.open_app(app_name)
        if app_name == SETTINGS:
            self.enter_text('Search', 'About')
            # try:
            #     self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value='Search').send_keys('About')
            # except Exception as e:
            #     print('Search about failed: {}'.format(str(e)))

            self.click_text('Cancel')
        elif app_name == TV:
            self.enter_text('Shows, Movies, and More', 'free')
            self.click_text('free tv shows')
            self.click_text('See TV Show')
            self.click_text('Play free Episode')

    def enter_text(self, text_field_name, text):
        try:
            self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value=text_field_name).send_keys(text)
        except Exception as e:
            print('Enter text failed: {}'.format(str(e)))

    def click_text(self, text):
        try:
            icon = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, text))
            )
            icon.click()
            print('Click text {}'.format(text))
        except Exception as e:
            print('Can not click text {} due to {}'.format(text, str(e)))

    def get_battery_level(self):
        result = self.driver.battery_info

        # out = result['stdout']
        # print(out)
        return result

    # only home, volumeUp, volumeDown supported.
    def home(self, times=1):
        for i in range(times):
            self.driver.press_button('HOME')
            sleep(0.1)

    def get_model(self):
        m = self.driver.capabilities['deviceName']
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
            touch.long_press(x=500, y=550).move_to(x=500, y=1800).release().perform()
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

    def get_egv(self):
        egv = ''
        try:
            egv = self.driver.find_element_by_id('com.dexcom.g7:id/id_glucose_compass_egv').text
        except NoSuchElementException as e:
            print('No EGV ' + str(e))
        finally:
            return egv

    def verify_and_ack_alert(self):
        ok = None
        try:
            ok = self.driver.find_element_by_id('com.dexcom.g7:id/id_alert_acknowledge_button')
        except NoSuchElementException as e:
            print('No Alert ok' + str(e))
        finally:
            if ok:
                ok.click()
                return True
            else:
                return False

    def g7_verify_signal_loss_message(self):
        """
        Verify signal loss after 10 minutes with message
        :return:
        """
        lost_help = lost_title = None
        try:
            lost_help = self.driver.find_element_by_id('com.dexcom.g7:id/id_glucose_state_card_help_button')
        except NoSuchElementException as e:
            print('Get lost_help button failed ' + str(e))

        try:
            lost_title = self.driver.find_element_by_id('com.dexcom.g7:id/id_glucose_state_card_title_label')
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

    def g7_verify_signal_loss_alert(self):
        """
        Verify signal loss after 20 minutes with message
        :return:
        """
        lost_ok = lost_title = None
        try:
            lost_ok = self.driver.find_element_by_id('com.dexcom.g7:id/id_alert_acknowledge_button')
        except NoSuchElementException as e:
            print('Get lost_ok button failed ' + str(e))

        try:
            lost_title = self.driver.find_element_by_id('com.dexcom.g7:id/id_alert_title_label')
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
