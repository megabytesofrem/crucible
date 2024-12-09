import fcntl
from io import BytesIO
from pathlib import Path

from PIL import Image
from gi.repository import GdkPixbuf

from model.enums import GameVariant

# Path to the lock file
lock_file_path = Path(Path.home() / ".crucible.lock")


def get_game_shortname(game: GameVariant):
    return GameVariant.serialize_to_id(game)


def place_lock():
    """Place a lockfile in /tmp to ensure we only have one instance running"""

    lock_file = open(lock_file_path, "w")
    # noinspection PyBroadException
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("Placed the lock")
    except:
        return None

    return lock_file


def destroy_lock():
    """Destroy the lockfile"""
    if lock_file_path.exists():
        print("Destroyed the lock")
        lock_file_path.unlink()


def load_banner_image(game: str, size=(300, 150)):
    try:  # 600 x 300
        image = Image.open(f"crucible_app/assets/banners/{game}.jpg")
    except FileNotFoundError:
        # Load a fallback image if the game banner is not found
        image = Image.open("crucible_app/assets/banners/default.jpg")

    # This is probably redundant, from when we were resizing the image
    # on the fly, should probably be removed at some point

    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Step 3: Load the bytes into a GdkPixbuf for GTK
    pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_type("png")
    pixbuf_loader.write(image_bytes.getvalue())
    pixbuf_loader.close()
    pixbuf = pixbuf_loader.get_pixbuf()

    return pixbuf
