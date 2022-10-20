from apython.appm import AppiumDevice


appium_d = AppiumDevice('R5CR411179D')
print(appium_d.driver.capabilities['deviceModel'])
appium_d.driver.keyevent(3)
appium_d.driver.activate_app('com.android.settings')
appium_d.appium_set_volume_percentages([68, 58, 48, 38])
appium_d.save_screen('/Users/tt0622/volume')



