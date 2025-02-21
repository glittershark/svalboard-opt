{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:

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
      gurobi-optimods
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

  gurobi-optimods = python3Packages.buildPythonPackage rec {
    pname = "gurobi-optimods";
    version = "2.3.1";
    pyproject = true;
    src = fetchFromGitHub {
      owner = "Gurobi";
      repo = "gurobi-optimods";
      rev = "refs/tags/v${version}";
      sha256 = "sha256-+6tQVCHW6vbdaV/YaetCmA0oTkKxF06aBZWiyVpJkiQ=";
    };

    build-system = with python3Packages; [ hatchling ];

    dependencies = with python3Packages; [
      gurobipy
      gurobipy-pandas
      numpy
      pandas
      scipy
    ];
  };

  python = pkgs.python3.withPackages pythonPackages;
in pkgs.mkShell { buildInputs = [ python ]; }
