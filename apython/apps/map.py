from apython.appm import AppiumDevice


class Map(AppiumDevice):
    def __init__(self):
        self.location = 'Chicago'
        pass

    def navigate(self):
        print('{}'.format(self.location))


# todo: call Map directly, if connection lost, will be rerunning.
# Map.navigate()
