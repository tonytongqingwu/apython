from apython.iosappium import AppiumIOS
from apython.utils import get_iphone_id


ios_id = get_iphone_id()
print(ios_id)
appium_d = AppiumIOS(ios_id)
print(appium_d.driver.capabilities['deviceName'])
print('battery')
print(appium_d.get_battery_level())
# appium_d.open_app('TV')
# appium_d.driver.find_element_by_name('Back').click()
try:
    appium_d.driver.find_element_by_name('Resume Episode').click()  # works
except Exception as e:
    print('e')

appium_d.driver.find_element_by_name('Search')
# appium_d.open_settings()  # works
# appium_d.open_map()
# appium_d.home()
# appium_d.driver.log
# appium_d.driver.find_element_by_name('Back')
# appium_d.driver.find_element_by_name('Camera').click()
# appium_d.driver.find_element_by_accessibility_id('Settings').click()
#
# appium_d.driver.find_element_by_name('TV').click()  # no
# # appium_d.driver.find_element_by_name('About').click()  # works
# appium_d.appium_touch_move_down()
# appium_d.appium_touch_move_up()
# appium_d.driver.keyevent('HOME')
# appium_d.driver.save_screenshot('/Users/tt0622/camera.png')



