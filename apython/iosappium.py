import os
import sys
import datetime
import base64
import re
import time
from word2number import w2n
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
CHROME = 'Safari'
G7_APP = 'Dexcom G7'
TV = 'TV'
SETTINGS = 'Settings'

APPS = [CAMERA, MAP, CHROME, G7_APP, SETTINGS, TV]
SCROLL_DUR_MS = 3000


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
        window_size = self.driver.get_window_size()
        print(window_size)
        self.scroll_y_top1 = window_size['height'] * 0.1
        self.scroll_y_top = window_size['height'] * 0.2
        self.scroll_y_bottom = window_size['height'] * 0.8
        self.scroll_y_middle = window_size['height'] * 0.5
        self.scroll_y_top2 = window_size['height'] * 0.25
        self.scroll_x = window_size['width'] * 0.5
        self.scroll_x1 = window_size['width'] * 0.1

    def open_app(self, app_name):
        self.home()
        self.touch.tap(None, self.scroll_x, self.scroll_y_top).perform()
        self.click_text('Close Picture in Picture')
        self.click_text('NotificationShortLookView')
        self.g7_click_ok_alert_ack()
        self.home()
        sleep(2)
        self.click_text(app_name)
        print('Open app {}'.format(app_name))

    def run_app(self, app_name):
        self.open_app(app_name)
        if app_name == SETTINGS:
            self.appium_touch_move_up()
            self.appium_touch_move_up()
            self.appium_touch_move_down()
            self.appium_touch_move_down()
        elif app_name == TV:
            self.enter_text('Search', 'free')
            self.click_text('Cancel')
            self.enter_text('Search', 'free')
            self.enter_text('Shows, Movies, and More', 'free')
            self.click_text('free tv shows')
            sleep(3)
            self.touch.tap(None, self.scroll_x, self.scroll_y_top2).perform()
            self.click_text('Resume Episode')
            self.click_text('Play free Episode')
            sleep(10)
        elif app_name == G7_APP:
            self.touch.tap(None, self.scroll_x1, self.scroll_y_top1).perform()
            self.click_text('Glucose')
        elif app_name == CHROME:
            self.enter_text('Address', 'www.Dexcom.com')
            self.appium_touch_move_up()
            self.appium_touch_move_up()
            self.appium_touch_move_down()
            self.appium_touch_move_down()
            self.enter_text('Address', 'www.google.com')
            self.appium_touch_move_up()
            self.appium_touch_move_up()
            self.appium_touch_move_down()
            self.appium_touch_move_down()
        elif app_name == CAMERA:
            print('CAM')
            for i in range(3):
                self.click_text('PhotoCapture')
        elif app_name == MAP:
            print('MAP')
            self.appium_touch_move_up()
            self.appium_touch_move_up()
            self.appium_touch_move_down()
            self.appium_touch_move_down()

    def enter_text(self, text_field_name, text):
        try:
            self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value=text_field_name).send_keys(text)
        except Exception as e:
            print('Enter text failed: {}'.format(str(e)))

    def click_text(self, text, wait=10):
        try:
            icon = WebDriverWait(self.driver, wait).until(
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
        self.driver.get_screenshot_as_file(f_name)

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
            egv = self.driver.find_element_by_accessibility_id('id_glucose_compass').text
        except NoSuchElementException as e:
            print('No EGV ' + str(e))
        finally:
            print('EGV is {}'.format(egv))
            m = re.search('You\'re (.+) milligrams', egv)
            if m:
                word = m.group(1).replace('-', ' ')
                egv = w2n.word_to_num(word)
                print(egv)
            return egv

    def g7_verify_signal_loss_message(self):
        """
        Verify signal loss after 10 minutes with message
        :return:
        """
        lost_help = lost_title = None
        try:
            lost_help = self.driver.find_elements_by_ios_predicate('id_glucose_state_card_help_button')
        except NoSuchElementException as e:
            print('Get lost_help button failed ' + str(e))

        try:
            lost_title = self.driver.find_elements_by_ios_predicate('id_glucose_state_card_title_label')
        except NoSuchElementException as e:
            print('Get lost_title  failed ' + str(e))

        if lost_help is not None and lost_title is not None:
            return True
        else:
            return False

    def g7_click_ok_alert_ack(self):
        self.click_text('OK')

    def g7_verify_signal_loss_alert(self):
        """
        Verify signal loss after 20 minutes with message
        :return:
        """
        lost_ok = lost_title = None
        try:
            lost_ok = self.driver.find_elements_by_ios_predicate('id_alert_acknowledge_button')
        except NoSuchElementException as e:
            print('Get lost_ok button failed ' + str(e))

        if lost_ok is not None:
            return True

    def appium_touch_move_up(self):
        self._y_scroll(self.scroll_y_top, self.scroll_y_bottom)

    def appium_touch_move_down(self):
        self._y_scroll(self.scroll_y_bottom, self.scroll_y_top)

    def _y_scroll(self, y_start, y_end):
        actions = TouchAction(self.driver)
        actions.long_press(None, self.scroll_x, y_start, SCROLL_DUR_MS)
        actions.move_to(None, self.scroll_x, y_end)
        actions.perform()