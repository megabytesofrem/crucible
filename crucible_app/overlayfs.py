import os
import shutil
import subprocess
from pathlib import Path

from model.enums import Storefront
from model.game_model import Game


def run_command(command):
    try:
        # Spawn the command asynchronously using subprocess.Popen
        proc = subprocess.Popen(
            command,
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
            print("Process succeeded")
            print(stdout.decode("utf-8"))
        else:
            print("Process failed")
            print(stderr.decode("utf-8"))
    except Exception as e:
        print(f"Error spawning process: {e}")


def find_game_dir(game: Game, storefront) -> Path:
    # Set CRUCIBLE_BASE_PATH to override the default path
    base_path = None
    game_path = None

    match storefront:
        case Storefront.GOG:
            # Locate where Heroic installs games, by default this is ~/Games/Heroic
            base_path = os.environ.get("CRUCIBLE_BASE_PATH") or os.path.expanduser("~/Games/Heroic")

        case Storefront.STEAM:
            # Locate where Steam installs games, by default this is ~/.steam/steam/steamapps/common
            base_path = os.environ.get("CRUCIBLE_BASE_PATH") or os.path.expanduser(
                "~/.steam/steam/steamapps/common"
            )
        case _:
            raise ValueError("Unsupported storefront, only GOG and Steam are supported")

    game_path = Path(base_path) / game.name
    return game_path


def flat_copy(target_subdir: str, upper_dir: Path, output_dir: Path):
    """
    Copy all files from the target subdirectory relative to the mod into output_dir, while flattening it
    """

    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterate through each folder in the upper_dir
    for mod_folder in upper_dir.iterdir():
        if mod_folder.is_dir():
            target_dir = mod_folder / target_subdir
            if target_dir.exists() and target_dir.is_dir():
                # Iterate through each file/subfolder in the target subdirectory
                for item in target_dir.iterdir():
                    if item.is_file():
                        shutil.copy2(item, output_dir)
                    elif item.is_dir():
                        for subitem in item.iterdir():
                            if subitem.is_file():
                                shutil.copy2(subitem, output_dir)


def mount_overlay(game: Game, storefront: Storefront):
    """
    Mount the game folder as OverlayFS to allow for non-destructive loading
    """

    # Unmount the overlay if it is already mounted
    unmount_overlay()
    game_path = find_game_dir(game, storefront)

    mods = Path("~/crucible/mods").expanduser()
    work = Path("~/crucible/overlay/work").expanduser()
    game_files = game_path.expanduser()
    merged = Path("/tmp/crucible/overlay/merged")

    mods.parent.mkdir(parents=True, exist_ok=True)
    work.parent.mkdir(parents=True, exist_ok=True)
    merged.parent.mkdir(parents=True, exist_ok=True)

    # Create a temporary directory to hold the merged mods
    merged_data = mods / "merged_data"
    merged_nvse = mods / "merged_nvse"
    merged_data.mkdir(parents=True, exist_ok=True)
    merged_nvse.mkdir(parents=True, exist_ok=True)

    flat_copy("Data", mods, merged_data)

    # copy_flat("NVSE", mods, merged_nvse)

    command = [
        "pkexec",
        "mount",
        "-t",
        "overlay",
        "overlay",
        f"-olowerdir={(game_files / "Data").as_posix()},upperdir={merged_data.as_posix()},workdir={work.as_posix()}",
        merged.as_posix(),
    ]

    run_command(command)


def unmount_overlay():
    mount_point = Path("/tmp/crucible/overlay/merged")

    if mount_point.is_mount():
        mods = Path("~/crucible/mods").expanduser()

        merged_data = mods / "merged_data"
        merged_nvse = mods / "merged_nvse"

        run_command(["rm", "-rf", merged_data.as_posix()])
        run_command(["rm", "-rf", merged_nvse.as_posix()])
        run_command(["pkexec", "umount", "/tmp/crucible/overlay/merged"])
