from gi.repository import GLib, Gtk, Gdk, Gio, GdkPixbuf
import gi

from state import State
from ui.locate_game_dialog import LocateGameDialog

gi.require_version("Gtk", "4.0")


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Puffin Mod Manager")
        self.set_size_request(600, 500)
        self.set_default_size(600, 500)

        self.props.show_menubar = False
        self.build_ui()

    def create_row(self, title, desc):
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        label = Gtk.Label(label=title, xalign=0)
        box.append(label)

        row.set_child(box)
        row.set_selectable(True)
        return row

    def show_about_dialog(self, widget):
        logo = Gio.File.new_for_path("icon.png")
        logo_texture = Gdk.Texture.new_from_file(logo)

        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_transient_for(self)

        self.about_dialog.set_modal(True)
        self.about_dialog.set_version("0.1.1")
        self.about_dialog.set_logo(logo_texture)
        self.about_dialog.set_copyright("2024 Puffin Mod Manager Developers")

        self.about_dialog.set_visible(True)

    def build_left_child(self):
        self.left_child = Gtk.ListBox()

        # for game in State.SUPPORTED_GAMES:
        #     self.left_child.append(self.create_row(f"{game}", f""))

    def build_right_child(self):
        self.right_child = Gtk.Label(label="Right Pane")

    def build_ui(self):
        """Build the UI for the main application window"""

        self.header = Gtk.HeaderBar(title_widget=Gtk.Label(label="Puffin Mod Manager"))
        self.header.pack_start(locate_game_button := Gtk.Button.new_from_icon_name("tab-new"))

        self.header.pack_end(about_button := Gtk.Button.new_from_icon_name("help-about"))

        self.set_titlebar(self.header)

        # Add click event
        locate_game_button.connect("clicked", self.on_locate_game_button_clicked)
        about_button.connect("clicked", self.show_about_dialog)

        self.split_pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.split_pane.set_position(180)

        self.build_left_child()
        self.build_right_child()

        # Set children
        self.split_pane.set_start_child(self.left_child)
        self.split_pane.set_end_child(self.right_child)
        self.set_child(self.split_pane)

    def on_locate_game_button_clicked(self, widget):
        print("Locate Game button clicked")

        def on_dialog_response(dialog, response):
            if response == Gtk.ResponseType.OK:
                print("OK")
            elif response == Gtk.ResponseType.CANCEL:
                print("Cancel")

            dialog.destroy()

        dialog = LocateGameDialog(parent=self)
        dialog.connect("response", on_dialog_response)
        dialog.show()
