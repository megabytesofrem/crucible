import sys

import gi
import pygame

import util
from view.main_window import MainWindow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib


class Main(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.megabytesofrem.crucible")
        GLib.set_application_name("Crucible")

        # Initialize Pygame, and exit if we cannot
        # noinspection PyBroadException
        try:
            pygame.init()
            pygame.joystick.init()
        except:
            exit(1)

        # Create a lockfile to ensure there is only one instance of us
        lock_file = util.place_lock()
        if lock_file is None:
            print("An instance of Crucible is already running, please close it")
            exit(1)
        else:
            self.lock_file = lock_file

    def on_window_destroy(self, window):
        print("Window closed, destroying the lock")
        self.lock_file.close()
        util.destroy_lock()

        self.quit()
        return False

    def do_activate(self):
        window = MainWindow(application=self)
        window.connect("close-request", self.on_window_destroy)
        # self.apply_stylesheet()
        window.present()

        # noinspection PyBroadException
        try:
            GLib.timeout_add(100, window.joystick.poll_joystick)
        except:
            pass


app = Main()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
