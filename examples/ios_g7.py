from apython.iosappium import *
from apython.utils import get_iphone_id
from datetime import datetime


ios_id = get_iphone_id()
print(ios_id)
appium_d = AppiumIOS(ios_id)
print(appium_d.driver.capabilities['deviceName'])
print('battery')
print(appium_d.get_battery_level())

# # appium_d.run_app(G1_APP)
# egv = appium_d.get_egv()
# print(egv)
# print(type(egv))
#
# if appium_d.g7_verify_signal_loss_alert():
#     print('alert')
# else:
#     print('no alert')
#
# appium_d.d1_g7_login('tst1.andr.us@gmail.com', 'Test1ng2022')
user_nm = 'gleon.vnv+004@gmail.com'
pass_wd = 'Dexcom123'

try:
    # appium_d.driver.find_element_by_ios_predicate(
    #     'value == "Username/E-mail address" AND type == "XCUIElementTypeTextField"').click()
    # sleep(2)
    # # should also work: appium_d.driver.find_element_by_ios_class_chain('**/XCUIElementTypeTextField[`value == "Username/E-mail address"`]').click()
    # appium_d.driver.find_element_by_ios_class_chain('**/XCUIElementTypeTextField[`value == "Username/E-mail address"`]').send_keys(user_nm)
    # appium_d.driver.find_element_by_ios_predicate('label == "Done"').click()  # works
    # appium_d.click_text('Next')

    # appium_d.driver.find_element_by_ios_class_chain('**/XCUIElementTypeWindow[3]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther[1]').click()
    # appium_d.driver.find_element_by_ios_class_chain('**/XCUIElementTypeWindow[3]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther[1]').send_keys(pass_wd)
    # appium_d.driver.find_element_by_ios_predicate('value == "Password"').click()
    # appium_d.driver.find_element_by_ios_predicate('value == "Password"').send_keys(pass_wd)
    # appium_d.driver.find_element_by_ios_predicate('label == "Done"').click()
    # appium_d.driver.find_element_by_ios_predicate('label == "Login"').click()
    # sleep(20)
    appium_d.driver.find_element_by_ios_class_chain('**/XCUIElementTypeWebView[`name == "id_legal_webview"`]/XCUIElementTypeWebView/XCUIElementTypeWebView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther').click()
    appium_d.driver.find_element_by_ios_class_chain('**/XCUIElementTypeWebView[`name == "id_legal_webview"`]/XCUIElementTypeWebView/XCUIElementTypeWebView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther').click()
    appium_d.driver.find_element_by_ios_predicate('label == "Submit"').click()
except Exception as e:
    print('Login failed ' + str(e))

# # appium_d.g7_click_ok_alert_ack()
# print(datetime.now())