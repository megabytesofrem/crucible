from gi.repository import Gtk

class StyledButton(Gtk.Button):
    def __init__(self, label, styles=[]):
        super().__init__(label=label)
        for style in styles:
            self.get_style_context().add_class(style)