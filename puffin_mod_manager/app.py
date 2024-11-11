from ui.main_window import MainWindow
from gi.repository import GLib, Gtk, Gdk
import sys
import gi

gi.require_version("Gtk", "4.0")


class Main(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.megabytesofrem.PuffinModManager")
        GLib.set_application_name("Puffin Mod Manager")

    def do_activate(self):
        window = MainWindow(application=self)
        window.present()


app = Main()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
