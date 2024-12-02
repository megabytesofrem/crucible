from typing import Optional

from gi.repository import Gtk


class ModalDialog(Gtk.Dialog):
    """
    Base class for custom, immovable modal dialogs that are always centered and on top
    of a parent window.
    """

    def __init__(self, parent, title: str):
        super().__init__(transient_for=parent, use_header_bar=False)

        self.title = title
        self.fake_header: Optional[Gtk.Box] = None
        self.vbox: Optional[Gtk.Box] = None
        self.set_decorated(False)
        self.set_titlebar(Gtk.Box())
        self.set_modal(True)
        self._layout_ui()

    def _layout_ui(self):
        # Fake it till we make it.
        # NOTE: Don't call this, use your own layout_ui function as this is called on __init__.
        #
        # Since GTK 4 will not allow us to make a modal dialog immovable, we need to create our
        # own window decoration.
        self.fake_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.fake_header.set_margin_start(10)
        self.fake_header.set_margin_top(10)
        self.fake_header.set_margin_end(10)

        left_child = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)
        left_child.append(title_label := Gtk.Label(label=self.title, hexpand=True))
        title_label.set_justify(Gtk.Justification.CENTER)

        close_button = Gtk.Button.new_from_icon_name("window-close-symbolic")
        close_button.get_style_context().add_class("circular")
        close_button.get_style_context().add_class("error")
        close_button.connect("clicked", lambda _: self.do_close(self))

        self.fake_header.append(left_child)
        self.fake_header.append(close_button)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.vbox.set_margin_bottom(10)

        self.vbox.append(self.fake_header)
        self.set_child(self.vbox)

    def get_modal_body(self):
        return self.vbox

    def set_modal_body(self, body: Gtk.Widget):
        self.vbox.append(body)
