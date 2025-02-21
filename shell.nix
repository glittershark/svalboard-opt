{ pkgs ? import (builtins.fetchTarball {
  url =
    "https://github.com/NixOS/nixpkgs/archive/31ff66eb77d02e9ac34b7256a02edb1c43fb9998.tar.gz";
  sha256 = "14a1rd8zk7ncgl453brj4hgg8axf8izviim5f5rpnagwkhhwxffx";
}) { config.allowUnfree = true; } }:

with pkgs;

let
  pythonPackages = ps:
    with ps; [
      pandas
      matplotlib
      numpy
      scikit-learn
      gurobipy
      networkx
      gurobipy-pandas
      ipython
    ];

  gurobipy-pandas = python3Packages.buildPythonPackage rec {
    pname = "gurobipy-pandas";
    version = "1.2.2";
    pyproject = true;
    src = fetchFromGitHub {
      owner = "Gurobi";
      repo = "gurobipy-pandas";
      rev = "refs/tags/v${version}";
      sha256 = "sha256-3QJ8L81NRo7la9p0kZkP//dj8w/1u994NF9iNzM2Gic=";
    };

    build-system = with python3Packages; [ hatchling ];

    dependencies = with python3Packages; [ gurobipy pandas ];
  };

  python = pkgs.python3.withPackages pythonPackages;
in pkgs.mkShell { buildInputs = [ python ]; }
