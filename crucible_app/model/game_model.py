from dataclasses import dataclass

from model.enums import GameVariant, Storefront
from proton import find_default_proton


@dataclass
class Game:
    """
    Game model to manage mods for
    """

    name: str
    enum_variant: GameVariant
    storefront: Storefront

    # Runner options
    proton_version: str
    proton_path: str
    installed_mods: list
    executable_path: str

    def __init__(self, name, enum_variant, storefront, executable_path):
        # Find a default Proton version
        self.name = name
        self.enum_variant = enum_variant
        self.storefront = storefront
        self.proton_version = ""
        self.installed_mods = []
        self.executable_path = executable_path

        find_default_proton()
