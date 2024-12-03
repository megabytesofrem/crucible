#!/bin/sh
# This script is copied to the built flatpak and invokes the main app

DIR="$(dirname "$0")"
cd "$DIR" || exit 1
exec python3 -B "$DIR"/crucible_app/app.py "$@"