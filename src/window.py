import pygetwindow
from time import sleep


class Window:
    def get_windows(self, window_name):
        return pygetwindow.getWindowsWithTitle(window_name)

    def activate_window(self, window):
        try:
            window.activate()
        except:
            window.minimize()
            window.maximize()

        sleep(2)
