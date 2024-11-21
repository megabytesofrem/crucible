from gi.repository import Gtk
from typing import Optional

from view.components.modal_dialog import ModalDialog
from model.backend import AppState

class ConfigureGameDialog(ModalDialog):
    def __init__(self, parent: Gtk.Window, title: str):
        super().__init__(parent=parent, title=title)
        self.state = AppState

        parent_width = parent.get_width()
        self.set_default_size(parent_width / 1.2, parent_width / 1.6)
        self.set_size_request(parent_width / 1.2, parent_width / 1.6)
        self.layout_ui()

    def layout_ui(self):
        #self.set_modal_body(Gtk.Label(label="Hello world", hexpand=True))
        pass