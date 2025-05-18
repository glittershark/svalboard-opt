#!/usr/bin/env sh

if [ "$1" != "--here" ]; then
    cd /home/aspen/svalboard-opt || exit
fi

nix-shell --run "python3 layout.py"
