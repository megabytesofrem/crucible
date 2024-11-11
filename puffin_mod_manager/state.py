from dataclasses import dataclass
from enum import Enum


class Game(Enum):
    FALLOUT_3 = "Fallout 3"
    FALLOUT_NEW_VEGAS = "Fallout New Vegas"
    FALLOUT_4 = "Fallout 4"
    SKYRIM = "Skyrim"
    SKYRIM_SE = "Skyrim Special Edition"

    def __str__(self):
        return self.value

    def from_string(string):
        match string:
            case "Fallout 3":
                return Game.FALLOUT_3
            case "Fallout New Vegas":
                return Game.FALLOUT_NEW_VEGAS
            case "Fallout 4":
                return Game.FALLOUT_4
            case "Skyrim":
                return Game.SKYRIM
            case "Skyrim Special Edition":
                return Game.SKYRIM_SE
            case _:
                raise ValueError("Unsupported game")


class Storefront(Enum):
    STEAM = "Steam"
    GOG = "GOG"

    def __str__(self):
        return self.value


@dataclass
class State:
    SUPPORTED_GAMES = [
        Game.FALLOUT_3, Game.FALLOUT_NEW_VEGAS, Game.FALLOUT_4, Game.SKYRIM, Game.SKYRIM_SE
    ]

    STOREFRONTS = [Storefront.STEAM, Storefront.GOG]
