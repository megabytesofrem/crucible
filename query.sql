CREATE TABLE "Game" (
    "id"    TEXT NOT NULL,
    "name"    TEXT NOT NULL,
    "storefront"    TEXT,
    "executable_path"    TEXT,
    PRIMARY KEY("id")
);

CREATE TABLE "InstalledMod" (
    "id"    TEXT NOT NULL,
    "name"    TEXT NOT NULL,
    "game_id"    TEXT NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("game_id") REFERENCES "Game"("id")
);