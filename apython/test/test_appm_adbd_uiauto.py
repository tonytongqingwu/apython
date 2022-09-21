from apython.adbd import AdbDevice
from apython.uiauto import UADevice
from apython.adbd import AdbDevice
from apython.appm import AppiumDevice


def test_volume():
    # adb_d = AdbDevice('R38MA09YRPM')
    # adb_d.key_five(4)
    # adb_d.start_app_settings()

    d = UADevice('573052324e573398')
    d.scroll_to_select('Sound')  # pixel3a
    # d.dump_screen('sound')
    d.scroll_to_select('Sounds and vibration')  # S9, S10
    d.drag(165, 301, 1036, 433, 10)  # Media
    d.drag(165, 536, 1036, 668, 10)

