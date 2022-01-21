from time import sleep
import gi
gi.require_version("Wnck", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Wnck, GdkX11, Gdk


class WindowLinux:
    def get_windows(self, window_name):
        screen = Wnck.Screen.get_default()
        screen.force_update()
        windows = screen.get_windows()
        result = []

        for window in windows:
            if window_name in window.get_name():
                result.append(window)

        return result

    def activate_window(self, window):
        now = GdkX11.x11_get_server_time(GdkX11.X11Window.lookup_for_display(Gdk.Display.get_default(),
                                                                             GdkX11.x11_get_default_root_xwindow()))

        window.activate(now)
        sleep(2)
