from time import sleep
from apython.appm import AppiumDevice


class G1(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def launch_g1(self):
        print("-------------------------------------")
        print("Launch G1")
        print("-------------------------------------")
        try:
            # os.system("adb -s " + self.adb_id + " shell am start -n com.dexcom.g7/com.dexcom.phoenix.ui.SplashActivity")
            self.home()
            self.driver.activate_app('com.dexcom.dexcomone')
            sleep(8)
        except Exception as e:
            print(str(e))
            print(type(e))
            self.back(5)
            if "A session is either terminated or not started" in str(e):
                self.server_error_recovery()
            if "An unknown server-side error" in str(e):
                self.driver.quit()
                sleep(2)
                self.server_error_recovery()
