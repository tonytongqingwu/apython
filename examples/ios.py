from apython.iosappium import *
from apython.utils import get_iphone_id


ios_id = get_iphone_id()
print(ios_id)
appium_d = AppiumIOS(ios_id)
print(appium_d.driver.capabilities['deviceName'])
print('battery')
print(appium_d.get_battery_level())

# appium_d.touch.tap(None, 30, 50).perform()
# appium_d.touch.tap(None, appium_d.scroll_x1, appium_d.scroll_y_top1).perform()
appium_d.run_app(G7_APP)


