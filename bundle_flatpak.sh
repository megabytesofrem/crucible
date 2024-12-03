#!/usr/bin/env bash

# Clean up the build directory
[ -d build/flatpak ] && rm -r build/flatpak

build_flatpak() {
  # Build a flatpak that can be installed locally
  flatpak-builder --install-deps-from=flathub --repo=local-repo --force-clean build com.megabytesofrem.Crucible.yml
  flatpak build-bundle local-repo Crucible.flatpak com.megabytesofrem.Crucible --runtime-repo=https://flathub.org/repo/flathub.flatpakrepo

  echo "Done. Run flatpak install --user Crucible.flatpak to install the flatpak."
}

build_flatpak