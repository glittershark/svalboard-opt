#!/usr/bin/env sh

cd /home/aspen/svalboard-opt || exit
nix-shell --run "python3 layout.py"
