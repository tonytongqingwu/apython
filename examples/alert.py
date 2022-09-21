from apython.appm import AppiumDevice


appium_d = AppiumDevice('573052324e573398', '4723', 'G7')

"""
This is part of script that you need check alert at any moment.
"""
appium_d.driver.activate_app('com.dexcom.g7')
appium_d.save_screen('/Users/tt0622/alert')
if appium_d.verify_signal_loss_alert():
    print('Has alert')
else:
    print('No alert')
