import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Proton:
    version: str
    path: str


def find_default_proton() -> Optional[Proton]:
    found_proton = False

    proton_version = ""
    proton_versions = _find_proton_versions()

    # Find the first and ideally most recent Proton version we
    while not found_proton:
        if "Proton Experimental" in proton_versions:
            proton_version = "Proton Experimental"
            found_proton = True
        elif "Proton 9.0" in proton_versions:
            proton_version = "Proton 9.0"
            found_proton = True
        elif "Proton 8.0" in proton_versions:
            proton_version = "Proton 8.0"
            found_proton = True
        elif "Proton 7.0" in proton_versions:
            proton_version = "Proton 7.0"
            found_proton = True
        elif "Proton 6.3" in proton_versions:
            proton_version = "Proton 6.3"
            found_proton = True
        else:
            # Could not find any Proton versions, HCF
            found_proton = False

    if found_proton:
        proton_path = proton_versions[proton_version]
        return Proton(proton_version, proton_path)


def find_proton_versions() -> list[Proton]:
    protons: list[Proton] = []
    _protons = _find_proton_versions()

    for ver, path in _protons:
        protons.append(Proton(ver, path))

    return protons


def _find_proton_versions() -> dict[str, str]:
    # Internal function used to gather proton versions, use find_proton_versions

    # Default directories to search for Proton versions
    default_dirs = {
        "Steam Proton": "~/.steam/steam/steamapps/common",
        "Custom Proton": "~/.steam/root/compatibilitytools.d",
    }

    proton_versions: dict[str, str] = {}
    for _, directory in default_dirs.items():
        directory = os.path.expanduser(directory)  # Expand ~ to the full path
        if os.path.exists(directory):
            # Check all subdirectories for Proton versions
            for dir_name in os.listdir(directory):
                full_path = os.path.join(directory, dir_name)
                if os.path.isdir(full_path) and dir_name.lower().startswith("proton"):
                    proton_versions[dir_name] = full_path

    return proton_versions
