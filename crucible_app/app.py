import sys

import gi
import pygame

from view.main_window import MainWindow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib


class Main(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.megabytesofrem.crucible")
        GLib.set_application_name("Crucible")

        # Initialize Pygame
        pygame.init()
        pygame.joystick.init()

    def do_activate(self):
        window = MainWindow(application=self)
        # self.apply_stylesheet()
        window.present()

        GLib.timeout_add(100, window.joystick.poll_joystick)


app = Main()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
