import sqlite3
from typing import List, Optional

from model.enums import GameVariant, Storefront
from model.game_model import Game

ALL_SUPPORTED_GAMES = [
    GameVariant.FALLOUT_3,
    GameVariant.FALLOUT_NEW_VEGAS,
    GameVariant.FALLOUT_4,
    GameVariant.SKYRIM,
    GameVariant.SKYRIM_SE,
]

ALL_STOREFRONTS = [Storefront.STEAM, Storefront.GOG]

SCHEMA_TABLE_GAME = """
CREATE TABLE IF NOT EXISTS "Game" (
    "id"    TEXT NOT NULL,
    "name"    TEXT NOT NULL,
    "storefront"    TEXT NOT NULL,
    "proton_version" TEXT NOT NULL,
    "proton_path" TEXT NOT NULL,
    "executable_path"    TEXT,
    PRIMARY KEY("id")
);
"""

SCHEMA_TABLE_INSTALLEDMOD = """
CREATE TABLE IF NOT EXISTS "InstalledMod"  (
    "id"    TEXT NOT NULL,
    "name"    TEXT NOT NULL,
    "game_id"    TEXT NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("game_id") REFERENCES "Game"("id")
);
"""


class Backend:
    def __init__(self):
        self.conn = sqlite3.connect("store.db")
        self.cursor = self.conn.cursor()
        self.setup_schema()

    def setup_schema(self):
        self.cursor.execute(SCHEMA_TABLE_GAME)
        self.cursor.execute(SCHEMA_TABLE_INSTALLEDMOD)

    def close_connection(self):
        self.conn.close()

    def insert_game(self, game: Game):
        self.cursor.execute(
            f"""
            INSERT INTO 'Game' (
                id, name, storefront, proton_version, proton_path, executable_path
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                game.enum_variant.serialize_to_id(),
                game.name,
                game.storefront.serialize_to_string(),
                game.proton_version,
                game.proton_path,
                game.executable_path,
            ),
        )
        self.conn.commit()

    def update_game_name(self, id: str, new_name: str):
        self.cursor.execute("UPDATE 'Game' SET name=? WHERE id=?", (new_name, id))

    def update_proton_version(self, id: str, proton_version: str, proton_path: str):
        self.cursor.execute(
            "UPDATE 'Game' SET proton_version=?, proton_path=? WHERE id=?",
            (proton_version, proton_path, id),
        )

    def remove_game(self, game: Game):
        self.cursor.execute("DELETE FROM 'Game' WHERE name=?", (game.name,))
        self.conn.commit()

    def get_all_games(self) -> List[Game]:
        self.cursor.execute("SELECT * FROM 'Game'")
        response = self.cursor.fetchall()
        games = []

        if response is None:
            return []

        for row in response:
            game = Game(
                enum_variant=GameVariant.id_to_variant(row[0]),
                name=row[1],
                storefront=Storefront.name_to_variant(row[2]),
                executable_path=row[3],
            )
            games.append(game)

        return games

    def get_game_by_id(self, id: str) -> Optional[Game]:
        self.cursor.execute(f"SELECT * FROM 'Game' WHERE id=?", (id,))
        response = self.cursor.fetchone()

        if response is None:
            return None

        return Game(
            enum_variant=GameVariant.name_to_variant(response[0]),
            name=response[1],
            storefront=Storefront.name_to_variant(response[2]),
            executable_path=response[3],
        )


class State:
    def __init__(self):
        self.db_backend = Backend()

        self.selected_game_name = ""
        self.selected_game_model: Optional[Game] = None

    def get_backend(self):
        return self.db_backend

    def set_selected_game_name(self, name):
        self.selected_game_name = name

    def set_selected_game_model(self, game):
        self.selected_game_model = game

    def get_selected_game_name(self):
        return self.selected_game_name

    def get_selected_game_model(self):
        return self.selected_game_model

    def get_store(self):
        return self.db_backend.get_all_games()


AppState = State()
