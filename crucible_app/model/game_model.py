from dataclasses import dataclass, field
from model.enums import GameVariant, Storefront


@dataclass
class Game:
    """
    Model for a game to manage installed mods
    """

    name: str
    enum_variant: GameVariant
    storefront: Storefront

    # List of installed mods
    installed_mods: list

    # Path to the game executable
    executable_path: str

    def __init__(self, name, enum_variant, storefront, executable_path):
        self.name = name
        self.enum_variant = enum_variant
        self.storefront = storefront
        self.installed_mods = []
        self.executable_path = executable_path
