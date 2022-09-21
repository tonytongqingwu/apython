from apython.appm import AppiumDevice


# appium_d = AppiumDevice('573052324e573398', '4723', 'G7')  # S9
appium_d = AppiumDevice('989AY13LAL', '4723', 'G7')
print(appium_d.driver.capabilities['deviceModel'])
appium_d.driver.keyevent(3)
appium_d.driver.activate_app('com.android.settings')
appium_d.appium_set_volume_percentages([68, 58, 48, 38])
appium_d.save_screen('/Users/tt0622/volume')



