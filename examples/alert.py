from apython.appm import AppiumDevice


appium_d = AppiumDevice('989AY13LAL', '4723', 'G7')

"""
This is part of script that you need check alert at any moment.
"""
appium_d.driver.activate_app('com.dexcom.g7')
appium_d.save_screen('/Users/tt0622/alert')

try:
    if appium_d.verify_signal_loss_alert():
        print('Has alert')
    else:
        print('No alert')
except Exception as e:
    print(e)
finally:
    print('find no alert')

try:
    if appium_d.verify_signal_loss_message():
        print('Has message')
    else:
        print('No message')
except Exception as e:
    print(e)
finally:
    print('Find no message')
