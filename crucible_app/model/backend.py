from dataclasses import dataclass
from typing import List
from gi.repository import GObject

import sqlite3

from model.enums import GameVariant, Storefront
from model.game_model import Game

ALL_SUPPORTED_GAMES = [
    GameVariant.FALLOUT_3,
    GameVariant.FALLOUT_NEW_VEGAS,
    GameVariant.FALLOUT_4,
    GameVariant.SKYRIM,
    GameVariant.SKYRIM_SE
]

ALL_STOREFRONTS = [Storefront.STEAM, Storefront.GOG]


class Backend:
    def __init__(self):
        self.conn = sqlite3.connect('store.db')
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def insert_game(self, game: Game):
        self.cursor.execute(f"INSERT INTO 'Game' (id, name, storefront, executable_path) VALUES ('{
                            game.enum_variant.serialize()}', '{game.name}', '{game.storefront}', '{game.executable_path}')")
        self.conn.commit()

    def remove_game(self, game: Game):
        self.cursor.execute(f"DELETE FROM 'Game' WHERE name='{game.name}'")
        self.conn.commit()

    def get_all_games(self) -> List[Game]:
        self.cursor.execute("SELECT * FROM 'Game'")
        response = self.cursor.fetchall()
        games = []

        if response is None:
            return []

        for row in response:
            game = Game(
                enum_variant=GameVariant.deserialize(row[0]),
                name=row[1],
                storefront=Storefront.serialize(row[2]),
                executable_path=row[3]
            )
            games.append(game)

        return games

    def get_game_by_id(self, id: str) -> Game:
        self.cursor.execute(f"SELECT * FROM 'Game' WHERE id='{id}'")
        response = self.cursor.fetchone()

        if response is None:
            return None

        return Game(
            enum_variant=GameVariant.deserialize(response[0]),
            name=response[1],
            storefront=Storefront.serialize(response[2]),
            executable_path=response[3]
        )


class State:
    def __init__(self):
        self.db_backend = Backend()

        self.selected_game_name = ""
        self.selected_game_model = None

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
