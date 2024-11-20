import io
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf
from PIL import Image

from model.backend import AppState, GameVariant
from view.util import get_game_shortname, load_banner_image
from view.locate_game_dialog import LocateGameDialog


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Crucible")
        self.set_size_request(600, 500)
        self.set_default_size(600, 500)

        self.props.show_menubar = False
        self.selected_game_model = None

        self.layout_ui()

    def show_about_dialog(self, widget):
        logo = Gio.File.new_for_path("icon.png")
        logo_texture = Gdk.Texture.new_from_file(logo)

        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_transient_for(self)

        self.about_dialog.set_modal(True)
        self.about_dialog.set_version("0.1.1")
        self.about_dialog.set_logo(logo_texture)
        self.about_dialog.set_copyright("© 2024 Crucible Developers")

        self.about_dialog.set_visible(True)

    def layout_game_list(self):
        self.game_list = Gtk.ListBox()
        self.game_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.game_list.connect("row-selected", self.on_selection_changed)

        # Load the game list from the backend
        backend = AppState.get_backend()
        for game in backend.get_all_games():
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=game.name, xalign=0)
            row.set_child(label)
            self.game_list.append(row)

    def layout_title_box(self):
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        selected_game = GameVariant.deserialize(AppState.get_selected_game_name())

        self.active_title_label = Gtk.Label(xalign=0)
        self.active_title_label.set_hexpand(True)
        self.active_title_label.set_markup(f"<span size='large'><b>No game selected</b></span>")

        # Title box contains the banner and the active title label
        title_box.append(self.active_title_label)
        launch_button = Gtk.Button(label="Launch")
        settings_button = Gtk.Button.new_from_icon_name("emblem-system")
        title_box.append(launch_button)
        title_box.append(settings_button)

        return title_box

    def layout_mod_view(self):
        self.game_options = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.game_options.set_margin_top(10)
        self.game_options.set_margin_start(10)
        self.game_options.set_margin_end(10)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        selected_game = GameVariant.deserialize(AppState.get_selected_game_name())

        self.banner = Gtk.Picture.new_for_pixbuf(load_banner_image(get_game_shortname(selected_game)))
        self.banner.set_content_fit(Gtk.ContentFit.FILL)

        title_box = self.layout_title_box()

        if selected_game is None:
            self.banner.set_visible(False)
            self.active_title_label.set_markup("<span size='large'><b>No game selected</b></span>")

        self.game_options.append(self.banner)
        self.game_options.append(title_box)

    def layout_ui(self):
        """Layout the UI for the main application window"""

        self.header = Gtk.HeaderBar(title_widget=Gtk.Label(label="Crucible"))
        self.header.pack_start(locate_game_button := Gtk.Button.new_from_icon_name("tab-new"))

        self.header.pack_end(about_button := Gtk.Button.new_from_icon_name("help-about"))

        self.set_titlebar(self.header)

        # Add click event
        locate_game_button.connect("clicked", self.on_locate_game_button_clicked)
        about_button.connect("clicked", self.show_about_dialog)

        self.split_pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.split_pane.set_position(180)

        self.layout_game_list()
        self.layout_mod_view()

        # Set children
        self.split_pane.set_start_child(self.game_list)
        self.split_pane.set_end_child(self.game_options)
        self.set_child(self.split_pane)

    # Signal handlers

    def on_selection_changed(self, listbox, row):
        selected_row = listbox.get_selected_row()
        if selected_row:
            label = selected_row.get_child()
            title = label.get_text()
            game = GameVariant.deserialize(title)

            selected_index = selected_row.get_index()

            # Update the application state
            AppState.set_selected_game_name(game.__str__())
            AppState.set_selected_game_model(AppState.get_store()[selected_index])
            self.selected_game_model = AppState.get_selected_game_model()

        self.on_update_ui(AppState, None)

    def on_update_ui(self, state, _):
        selected_game = GameVariant.deserialize(AppState.get_selected_game_name())
        if selected_game:
            self.active_title_label.set_markup(f"<span size='large'><b>{selected_game.__str__()}</b></span>")

            self.banner.set_visible(True)
            self.banner.set_pixbuf(load_banner_image(get_game_shortname(selected_game)))

    def on_locate_game_button_clicked(self, widget):
        def response(dialog, response):
            state = AppState
            backend = AppState.get_backend()

            if response == Gtk.ResponseType.OK:
                # Create the listbox row
                selected_game = state.get_selected_game_model()
                unique_id = selected_game.enum_variant.serialize()

                print("Unique ID:", unique_id)
                print("Query: ", backend.get_game_by_id(unique_id))

                if backend.get_game_by_id(unique_id) is None:
                    row = Gtk.ListBoxRow()
                    label = Gtk.Label(label=selected_game.name, xalign=0)
                    row.set_child(label)
                    self.game_list.append(row)
                    backend.insert_game(selected_game)

            elif response == Gtk.ResponseType.CANCEL:
                print("Cancel")

            dialog.destroy()

        dialog = LocateGameDialog(parent=self)
        dialog.connect("response", response)
        dialog.show()
