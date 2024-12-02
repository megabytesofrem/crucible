from gi.repository import Gtk


class RowItem(Gtk.ListBoxRow):
    hbox: Gtk.Box
    prefix_label: Gtk.Label
    widget: Gtk.Widget

    def __init__(self, prefix_label: Gtk.Label, widget: Gtk.Widget):
        super().__init__()

        self.prefix_label = prefix_label
        self.widget = widget
        self.set_selectable(True)
        self.layout_ui()

    def get_prefix_label(self) -> Gtk.Label:
        """Return the prefix label widget for the RowItem"""
        return self.prefix_label

    def get_widget(self) -> Gtk.Widget:
        """Return the widget for the RowItem"""
        return self.widget

    def layout_ui(self):
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hbox.set_margin_start(10)
        self.hbox.set_margin_end(10)
        self.hbox.set_margin_top(5)
        self.hbox.set_margin_bottom(5)

        self.hbox.append(self.prefix_label)
        self.hbox.append(self.widget)

        self.set_child(self.hbox)