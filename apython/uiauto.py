from uiautomator import Device


class UADevice:
    def __init__(self, adb_id):
        self.adb_id = adb_id
        self.d = Device(adb_id)

    def select_text(self, text):
        try:
            self.d(text=text).click
        except Exception as e:
            print('{} is not clickable, {}'.format(text, e))

    def scroll_to_select(self, text):
        if self.d(text=text).exists:
            self.d(text=text).click()
        else:
            try:
                self.d(scrollable=True).scroll.to(text=text)
                self.d(text=text).click()
            except Exception as e:
                print('{} is not selectable or clickable, {}'.format(text, e))

    def dump_screen(self, screen_name):
        screen_name_file = '{}_{}'.format(self.adb_id, screen_name)
        self.d.screenshot('{}.png'.format(screen_name_file))
        self.d.dump('{}.xml'.format(screen_name_file))
        # or get the dumped content(unicode) from return.
        # xml = self.d.dump()
        # print(xml)

    def drag(self, sx, sy, ex, ey, steps):
        self.d.drag(sx, sy, ex, ey, steps=steps)
