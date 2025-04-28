{ }:
import (builtins.fetchTarball {
  url =
    "https://github.com/NixOS/nixpkgs/archive/31ff66eb77d02e9ac34b7256a02edb1c43fb9998.tar.gz";
  sha256 = "14a1rd8zk7ncgl453brj4hgg8axf8izviim5f5rpnagwkhhwxffx";
}) { config.allowUnfree = true; }
