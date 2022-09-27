from time import sleep
from apython.appm import AppiumDevice


class Camera(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def take_pictures(self):
        print("Opening Camera Capture Photo")
        print("-------------------------------------")
        sleep(2)
        try:
            print("Open Camera capture photo")
            if 'Pixel' in self.driver.capabilities['deviceModel']:
                # self.driver.activate_app('com.google.android.GoogleCamera')  # pixel3a
                self.driver.start_activity('com.google.android.GoogleCamera', 'com.android.camera.CameraLauncher')
            else:
                self.driver.keyevent(27)
            sleep(4)

            for i in range(16):
                if 'Pixel' in self.driver.capabilities['deviceModel']:
                    self.driver.find_element_by_id('com.google.android.GoogleCamera:id/shutter_button').click()
                else:
                    self.driver.keyevent(27)
                sleep(0.5)
            self.home()
            print("Exit: Open_Camera")
        except Exception as e:
            print(str(e))
            print(type(e))
            self.back(5)
            self.home()
            if "A session is either terminated or not started" in str(e):
                self.server_error_recovery()
            if "An unknown server-side error" in str(e):
                self.driver.quit()
                sleep(2)
                self.server_error_recovery()
        finally:
            print('Done Camera')



