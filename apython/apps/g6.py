from time import sleep
from apython.appm import AppiumDevice


class G6(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def launch_g6(self):
        print("-------------------------------------")
        print("Launch G6")
        print("-------------------------------------")
        try:
            self.home()
            self.driver.activate_app('com.dexcom.g6')
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
