from gi.repository import Gtk

from model.backend import AppState
from model.game_model import Game
from proton import _find_proton_versions
from view.components.modal_dialog import ModalDialog
from view.components.row_item import RowItem
from view.components.styled_button import StyledButton


class ConfigureGameDialog(ModalDialog):
    vbox: Gtk.Box
    banner: Gtk.Picture
    listbox: Gtk.Box
    name_entry_row: RowItem
    path_entry_row: RowItem
    proton_ver_row: RowItem
    button_box: Gtk.Box

    selected_model: Game

    proton_versions: list[(str, str)]
    proton_version_strings: Gtk.StringList

    def __init__(self, parent: Gtk.Window, title: str):
        super().__init__(parent=parent, title=title)
        self.selected_model = AppState.get_selected_game_model()

        parent_width = parent.get_width()
        original_height = self.get_height()

        self.set_default_size(parent_width / 1.4, original_height + 100)
        self.set_size_request(parent_width / 1.4, original_height + 100)
        self.layout_ui()

    def layout_ui(self):
        self.vbox = self.get_modal_body()

        desc_label = Gtk.Label(
            label=f"Configure properties for {self.selected_model.name}", xalign=0
        )
        desc_label.set_margin_start(10)

        self.vbox.append(desc_label)

        # List of config options
        self.listbox = Gtk.ListBox(hexpand=True)
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.get_style_context().add_class("boxed-list-separate")

        # Name
        name_entry_label = Gtk.Label(label="Game Name  ", xalign=0, hexpand=False)
        name_entry_widget = Gtk.Entry(hexpand=True)
        name_entry_widget.set_text(self.selected_model.name)
        self.name_entry_row = RowItem(prefix_label=name_entry_label, widget=name_entry_widget)
        self.listbox.append(self.name_entry_row)

        # Path
        path_entry_label = Gtk.Label(label="Executable Path", xalign=0, hexpand=False)
        path_entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        path_entry_widget = Gtk.Entry(hexpand=True)
        path_browse_button = Gtk.Button.new_from_icon_name("folder-open")

        if self.selected_model.executable_path != "":
            path_entry_widget.set_text(self.selected_model.executable_path)
        else:
            path_entry_widget.set_placeholder_text("Select an executable path")

        path_entry_box.append(path_entry_widget)
        path_entry_box.append(path_browse_button)
        self.path_entry_row = RowItem(prefix_label=path_entry_label, widget=path_entry_box)
        self.listbox.append(self.path_entry_row)

        # Proton Version
        proton_ver_label = Gtk.Label(label="Proton Version", xalign=0, hexpand=False)
        proton_ver_dropdown = Gtk.DropDown(hexpand=True)
        self.proton_ver_row = RowItem(prefix_label=proton_ver_label, widget=proton_ver_dropdown)
        self.listbox.append(self.proton_ver_row)

        # Populate the string list
        self.proton_version_strings = Gtk.StringList()
        for version in _find_proton_versions().keys():
            self.proton_version_strings.append(version)

        proton_ver_dropdown.set_model(self.proton_version_strings)
        proton_ver_dropdown.set_selected(0)

        self.vbox.append(self.listbox)

        # Buttons
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, hexpand=True)
        self.button_box.set_margin_start(10)
        self.button_box.set_margin_end(10)
        self.button_box.set_margin_bottom(10)

        install_skse_button = StyledButton(label="Install NVSE/SKSE/SFSE")
        install_skse_button.set_hexpand(True)
        install_skse_button.connect("clicked", self.on_install_skse_clicked)

        apply_changes_button = StyledButton(label="Apply changes", styles=["suggested-action"])
        apply_changes_button.set_hexpand(True)
        apply_changes_button.connect("clicked", self.on_apply_changes_clicked)

        self.button_box.append(install_skse_button)
        self.button_box.append(apply_changes_button)

        self.vbox.append(self.button_box)

    def on_install_skse_clicked(self, button):
        self.response(Gtk.ResponseType.OK)

    def on_apply_changes_clicked(self, button):
        # Query the ID of the selected game
        # selected_id = self.selected_model.enum_variant.serialized()

        # Write changes to the database
        backend = AppState.get_backend()

        name_entry: Gtk.Entry = self.name_entry_row.get_widget()
        proton_ver_dropdown: Gtk.DropDown = self.proton_ver_row.get_widget()

        proton_string = self.proton_version_strings.get_string(proton_ver_dropdown.get_selected())

        # Update the name if it has been changed since
        # print(selected_id)

        self.response(Gtk.ResponseType.OK)
