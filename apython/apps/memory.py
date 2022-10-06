from time import sleep
from apython.appm import AppiumDevice


class MemoryFill(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def fill_memory(self):
        print("-------------------------------------")
        print("Memory Fill App is opened")
        print("-------------------------------------")
        try:
            self.driver.start_activity('com.rektgames.memoryfill', 'com.rektgames.memoryfill.Views.TabbedActivity')
            sleep(4)
        except Exception as e:
            print('Can not start memory fill app')
            print(str(e))
            print(type(e))
            return

        try:
            print("Click on ++100MB Button")
            for i in range(8):
                self.driver.find_element_by_id("com.rektgames.memoryfill:id/more").click()
                sleep(0.1)
            sleep(10)

            print("Click on Fill Button")
            for i in range(8):
                self.driver.find_element_by_id("com.rektgames.memoryfill:id/allocate").click()
                sleep(0.1)
            sleep(10)
            print("Exit: MemoryFill_App")
            print("____________________________________________________________________\n")
            self.back(5)
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
        finally:
            print('Done fill memory')
