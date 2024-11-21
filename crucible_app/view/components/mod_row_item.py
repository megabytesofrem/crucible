from gi.repository import Gtk

from model.game_model import Game
from typing import Optional


class ModRowItem(Gtk.ListBoxRow):
    def __init__(self, game_model: Optional[Game], mod):
        super().__init__()

        self.mod_name_label: Optional[Gtk.Label] = None
        self.hbox: Optional[Gtk.Box] = None
        self.remove_button: Optional[Gtk.Button] = None

        self.game_model: Optional[Game] = game_model
        self.mod = mod

        self.set_selectable(True)
        self.layout_ui()

    def layout_ui(self):
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.mod_name_label = Gtk.Label(label=self.mod, xalign=0, hexpand=True)
        self.remove_button = Gtk.Button.new_from_icon_name("list-remove-symbolic")
        
        self.hbox.append(self.mod_name_label)
        self.hbox.append(self.remove_button)

        self.set_child(self.hbox)