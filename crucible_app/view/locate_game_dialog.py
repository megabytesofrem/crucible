import io
from gi.repository import Gtk, GdkPixbuf
from PIL import Image

from model.backend import ALL_SUPPORTED_GAMES, AppState
from model.enums import GameVariant, Storefront
from model.game_model import Game
from view.util import get_game_shortname, load_banner_image


class LocateGameDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(transient_for=parent, use_header_bar=False)

        self.set_title("Locate Game")
        self.set_modal(True)

        self.set_default_size(400, 400)
        self.set_size_request(400, 400)
        self.layout_ui()

    def layout_ui(self):
        """Layout the UI for the locate game dialog"""

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.vbox.set_margin_top(10)
        self.vbox.set_margin_start(10)
        self.vbox.set_margin_end(10)

        self.set_child(self.vbox)

        # FIXME: Fix banner scaling (it is too large and won't scale down)
        self.banner = Gtk.Picture.new_for_pixbuf(load_banner_image("default"))

        # Stretch to fill container
        self.banner.set_content_fit(Gtk.ContentFit.FILL)

        self.vbox.append(self.banner)

        self.path_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.layout_path_entry()

        # Buttons for the dialog
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        self.button_box.append(confirm_button := Gtk.Button(label="Add Game"))
        self.button_box.append(cancel_button := Gtk.Button(label="Cancel"))
        confirm_button.get_style_context().add_class("primary-action")

        confirm_button.connect("clicked", self.on_confirm_clicked)
        cancel_button.connect("clicked", self.on_cancel_clicked)

        self.vbox.append(self.button_box)

    def layout_path_entry(self):
        # Drop down for selecting the game
        self.vbox.append(Gtk.Label(label="Select the game you want to add", xalign=0))
        self.game_dropdown = Gtk.DropDown()

        self.game_dropdown.connect("notify::selected-item", self.on_selection_changed)
        self.string_list = Gtk.StringList()

        for game in ALL_SUPPORTED_GAMES:
            self.string_list.append(game.__str__())

        self.game_dropdown.set_model(self.string_list)
        self.vbox.append(self.game_dropdown)

        # Game executable path entry
        self.vbox.append(Gtk.Label(label="Path to the game executable", xalign=0))

        self.path_entry = Gtk.Entry(placeholder_text="Game Path")
        self.path_entry.set_hexpand(True)
        self.browse_button = Gtk.Button.new_from_icon_name("folder-open")
        self.path_hbox.append(self.path_entry)
        self.path_hbox.append(self.browse_button)

        self.vbox.append(self.path_hbox)

    def on_confirm_clicked(self, button):
        self.response(Gtk.ResponseType.OK)

    def on_cancel_clicked(self, button):
        self.response(Gtk.ResponseType.CANCEL)

    def on_selection_changed(self, dropdown, _):
        selected_item = dropdown.get_selected_item()
        if selected_item:
            game_variant = GameVariant.deserialize(selected_item.get_string())
            game = Game(selected_item.get_string(), game_variant, Storefront.STEAM, "")

            AppState.set_selected_game_name(game_variant.__str__())
            AppState.set_selected_game_model(game)
            shortname = get_game_shortname(game_variant)
        else:
            shortname = "default"

        self.banner.set_pixbuf(load_banner_image(shortname))