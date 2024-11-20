from enum import Enum


class GameVariant(Enum):
    FALLOUT_3 = "Fallout 3"
    FALLOUT_NEW_VEGAS = "Fallout New Vegas"
    FALLOUT_4 = "Fallout 4"
    SKYRIM = "Skyrim"
    SKYRIM_SE = "Skyrim Special Edition"

    def __str__(self) -> str:
        return self.value

    def deserialize(string):
        match string:
            case "Fallout 3":
                return GameVariant.FALLOUT_3
            case "Fallout New Vegas":
                return GameVariant.FALLOUT_NEW_VEGAS
            case "Fallout 4":
                return GameVariant.FALLOUT_4
            case "Skyrim":
                return GameVariant.SKYRIM
            case "Skyrim Special Edition":
                return GameVariant.SKYRIM_SE
            case _:
                return None

    def serialize(self):
        match self:
            case GameVariant.FALLOUT_3:
                return "fallout3"
            case GameVariant.FALLOUT_NEW_VEGAS:
                return "falloutnv"
            case GameVariant.FALLOUT_4:
                return "fallout4"
            case GameVariant.SKYRIM:
                return "skyrim"
            case GameVariant.SKYRIM_SE:
                return "skyrimse"


class Storefront(Enum):
    STEAM = "Steam"
    GOG = "GOG"

    def __str__(self) -> str:
        return self.value

    def serialize(string):
        match string:
            case "Steam":
                return Storefront.STEAM
            case "GOG":
                return Storefront.GOG
            case _:
                return None
