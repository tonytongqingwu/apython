from apython.iosappium import *
from apython.utils import get_iphone_id
from datetime import datetime


ios_id = get_iphone_id()
print(ios_id)
appium_d = AppiumIOS(ios_id, dexcom_app_type=G1_APP)
print(appium_d.driver.capabilities['deviceName'])
print('battery')
print(appium_d.get_battery_level())

# appium_d.run_app(G1_APP)
egv = appium_d.get_egv()
print(egv)
print(type(egv))

if appium_d.g7_verify_signal_loss_alert():
    print('alert')
else:
    print('no alert')

# appium_d.d1_login('allanprodvnvbell@gmail.com', 'Dexcom123')
# appium_d.g7_click_ok_alert_ack()
print(datetime.now())