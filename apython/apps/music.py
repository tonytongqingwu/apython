from time import sleep
from apython.appm import AppiumDevice


class Music(AppiumDevice):
    def __init__(self):
        super().__init__()
        pass

    def appium_youtube_music(self, play_time):
        self.driver.activate_app('com.google.android.apps.youtube.music')
        sleep(3)
        try:
            print("Click on search icon")
            # self.driver.find_element_by_xpath(".//android.widget.ImageView[@content-desc='Search']").click()
            self.driver.find_element_by_id('com.google.android.apps.youtube.music:id/action_search_button').click()
            sleep(3)
            search_text = 'two hours soulful medidation'
            edit = self.driver.find_element_by_id('com.google.android.apps.youtube.music:id/search_edit_text')
            # edit = self.driver.find_element_by_xpath(".//android.widget.EditText").send_keys(search_text)
            edit.send_keys(search_text)
            self.enter()
            sleep(3)
            print("Scrolling Up and Down")
            self.appium_touch_move_up()
            sleep(1)
            self.appium_touch_move_up()
            sleep(1)
            self.appium_touch_move_down()
            sleep(1)
            print("Click on Video to Play")
            self.driver.find_element_by_xpath(".//android.view.ViewGroup[@index='0']").click()
            try:
                self.driver.find_element_by_id("com.google.android.youtube:id/skip_ad_button_container").click()
            except Exception as e:
                print("No ad")
            finally:
                print('Start music')

            sleep(play_time)
            sleep(3)
            print("Closing the Video")
            print("Exit: Youtube Music")
            print("____________________________________________________________________\n")
            self.back(10)
        except Exception as e:
            print('Music errors: ')
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
            print('Done music')
            self.back(5)
            self.home()