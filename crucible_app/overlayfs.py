import glob
import os
import subprocess

from model.enums import GameVariant, Storefront


def shell(command):
    return subprocess.run(
        command.split(" "), shell=True, check=True, stdout=subprocess.PIPE
    ).stdout.decode("utf-8")


class OverlayFS:
    """
    Utilities for working with mods and overlaying them as an OverlayFS
    file system.
    """

    def find_game_dir(self, game, storefront):
        # Set CRUCIBLE_BASE_PATH to override the default path: for games installed in non-standard locations
        base_path = None
        game_path = None

        match storefront:
            case Storefront.GOG:
                # Locate where Heroic installs games, by default this is ~/Games/Heroic
                base_path = os.environ.get("CRUCIBLE_BASE_PATH") or os.path.expanduser(
                    "~/Games/Heroic"
                )
            case Storefront.STEAM:
                # Locate where Steam installs games, by default this is ~/.steam/steam/steamapps/common
                base_path = os.environ.get("CRUCIBLE_BASE_PATH") or os.path.expanduser(
                    "~/.steam/steam/steamapps/common"
                )
            case _:
                raise ValueError("Unsupported storefront, only GOG and Steam are supported")

        game_path = glob.glob(f"{base_path}/*{game.get_friendly_name()}*")
        return game_path

    def find_mods(self, game):
        mod_list = glob.glob(f"~/crucible/mods/{game.get_friendly_name()}/*")
        return mod_list

    def coalesce_mods(self, game):
        mod_list = self.find_mods(game)
        mod_string = mod_list.join(":")
        return mod_string

    def mount_overlay(self, game, storefront):
        # Work directory is the temporary directory for staging the overlay
        # Upper directory is the directory where the original game files are stored
        # Lower directory is the directory where the mods are stored
        # Mount point is the directory where the overlay will be mounted

        game_path = self.find_game_dir(game, storefront)
        work_dir = "/tmp/crucible/overlay/work"
        mount_point = "/tmp/crucible/overlay/merged"

        # Walk through the mods directory and find all the mods
        match game:
            case GameVariant.FALLOUT_3:
                upper_dir = f"{game_path}/Data"
                lower_dir = f"{game_path}/Data"
            case GameVariant.FALLOUT_NEW_VEGAS:
                upper_dir = f"{game_path}/Data"
                lower_dir = f"{game_path}/Data"
            case GameVariant.FALLOUT_4:
                upper_dir = f"{game_path}/Data"
                lower_dir = f"{game_path}/Data"
            case GameVariant.SKYRIM:
                upper_dir = f"{game_path}/Data"

        # Coalesce the mods into a single string separated by colons
        init_lower_dir = lower_dir
        coalesced_mods = self.coalesce_mods(game)
        lower_dir = f"{init_lower_dir}:{coalesced_mods}"

        # Mount the overlay
        shell(f"mkdir -p {work_dir}")
        shell(f"mkdir -p {mount_point}")

        if not os.path.ismount(mount_point):
            shell(
                f"pkexec mount -t overlay overlay -o lowerdir={
                  lower_dir},upperdir={upper_dir},workdir={work_dir} {mount_point}"
            )

    def unmount_overlay():
        shell("pkexec umount /tmp/crucible/overlay/merged")
