import io
from gi.repository import Gtk, GdkPixbuf
from PIL import Image
import gi

from state import Game, State
gi.require_version("Gtk", "4.0")


class LocateGameDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(transient_for=parent, use_header_bar=False)

        self.set_title("Locate Game")
        self.set_modal(True)

        self.set_default_size(400, 400)
        self.set_size_request(400, 400)
        self.build_ui()

    def get_game_shortname(self, game):
        match game:
            case Game.FALLOUT_3:
                return "fallout3"
            case Game.FALLOUT_NEW_VEGAS:
                return "falloutnv"
            case Game.FALLOUT_4:
                return "fallout4"
            case _:
                return "default"

    def load_banner_image(self, game, size=(300, 150)):
        try:  # 600 x 300
            image = Image.open(f"puffin_mod_manager/ui/banners/{game}.jpg")
        except FileNotFoundError:
            # Load a fallback image if the game banner is not found
            image = Image.open("puffin_mod_manager/ui/banners/default.jpg")

        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        # Step 3: Load the bytes into a GdkPixbuf for GTK
        pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        pixbuf_loader.write(image_bytes.getvalue())
        pixbuf_loader.close()
        pixbuf = pixbuf_loader.get_pixbuf()

        return pixbuf

    def build_ui(self):
        """Build the UI for the locate game dialog"""

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.vbox.set_margin_top(10)
        self.vbox.set_margin_start(10)
        self.vbox.set_margin_end(10)

        self.set_child(self.vbox)

        # FIXME: Fix banner scaling (it is too large and won't scale down)
        self.banner = Gtk.Picture.new_for_pixbuf(self.load_banner_image("default"))

        # Stretch to fill container
        self.banner.set_content_fit(Gtk.ContentFit.FILL)

        self.vbox.append(self.banner)

        self.path_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.build_path_entry()

        # Buttons for the dialog
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        self.button_box.append(confirm_button := Gtk.Button(label="Add Game"))
        self.button_box.append(cancel_button := Gtk.Button(label="Cancel"))
        confirm_button.get_style_context().add_class("primary-action")

        confirm_button.connect(
            "clicked", lambda a: self.response(Gtk.ResponseType.OK))
        cancel_button.connect(
            "clicked", lambda a: self.response(Gtk.ResponseType.CANCEL))

        self.vbox.append(self.button_box)

    def build_path_entry(self):
        # Drop down for selecting the game
        self.vbox.append(Gtk.Label(label="Select the game you want to add", xalign=0))
        self.game_dropdown = Gtk.DropDown()

        self.game_dropdown.connect("notify::selected-item", self.on_selection_changed)
        self.string_list = Gtk.StringList()

        for game in State.SUPPORTED_GAMES:
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

    def on_selection_changed(self, dropdown, _):
        selected_item = dropdown.get_selected_item()
        if selected_item:
            game = Game.from_string(selected_item.get_string())
            shortname = self.get_game_shortname(game)

        else:
            shortname = "default"

        self.banner.set_pixbuf(self.load_banner_image(shortname))
