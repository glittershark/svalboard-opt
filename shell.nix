{ pkgs ? import ./nixpkgs.nix { } }:

with pkgs;

let
  pythonPackages = ps:
    with ps; [
      pandas
      matplotlib
      numpy
      pypdf
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
