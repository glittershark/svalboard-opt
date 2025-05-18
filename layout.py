#!/usr/bin/env python3

import os

os.environ["GRB_LICENSE_FILE"] = f"{os.getcwd()}/gurobi.lic"
print(os.getenv("GRB_LICENSE_FILE"))

import gurobipy as gp
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
import itertools
import collections

from letter_weights import LetterWeights

MODEL_FILE = "./model.mps"


@dataclass
class Keyboard:
    keys: list[int] = field(default_factory=lambda: [*range(27)])
    key_costs: list[int] = field(default_factory=lambda: [*np.abs(np.random.randn(27))])
    key_transfer_costs: list[list[int]] = field(
        default_factory=lambda: np.abs(np.random.randn(27, 27))
    )

    @classmethod
    def random(cls):
        return cls(
            key_costs=[*np.abs(np.random.randn(27))],
            key_transfer_costs=np.abs(np.random.randn(27, 27)),
        )


@dataclass
class KeyboardLayout:
    keyboard: Keyboard
    key_assignments: list[str]

    def assigned_letter(self, key: int) -> str:
        return self.key_assignments[letter]

    def assigned_key(self, letter: str) -> int:
        return self.key_assignments.index(letter)

    def __repr__(self):
        keys = ",\n".join(f"{i} = {k}" for (i, k) in enumerate(self.key_assignments))
        return f"KeyboardLayout(\n{keys}\n)"


def find_optimal_layout(
    keyboard: Keyboard, letter_weights: LetterWeights
) -> KeyboardLayout:
    if os.path.exists(MODEL_FILE):
        print(f"Resuming from previously saved model at {MODEL_FILE}")
        m = gp.read(MODEL_FILE)
    else:
        m = gp.Model()

        keys_to_letters = m.addVars(
            letter_weights.all_letters(), keyboard.keys, vtype=gp.GRB.BINARY
        )

        m.addConstrs(
            (
                sum(keys_to_letters[letter, key] for key in keyboard.keys) == 1
                for letter in letter_weights.all_letters()
            ),
            name="each letter assigned once",
        )

        m.addConstrs(
            (
                sum(
                    keys_to_letters[letter, key]
                    for letter in letter_weights.all_letters()
                )
                == 1
                for key in keyboard.keys
            ),
            name="each key assigned once",
        )

        def key_letter_weight(letter, key):
            return letter_weights.letters[letter] * keyboard.key_costs[key]

        def digraph_weight(digraph, key_pair):
            return (
                letter_weights.digraphs[digraph] * keyboard.key_transfer_costs[key_pair]
            )

        m.setObjective(
            sum(
                key_letter_weight(letter, key) * keys_to_letters[letter, key]
                for letter in letter_weights.all_letters()
                for key in keyboard.keys
            )
            + sum(
                digraph_weight(digraph, (key1, key2))
                * keys_to_letters[digraph[0], key1]
                * keys_to_letters[digraph[1], key2]
                for digraph in letter_weights.all_digraphs()
                for key1 in keyboard.keys
                for key2 in keyboard.keys
            ),
            sense=gp.GRB.MINIMIZE,
        )

    try:
        m.optimize(callback=lambda model, _: model.write(MODEL_FILE))
    except KeyboardInterrupt:
        model.write("./model.mps")
        raise

    key_assignments = [None for _ in range(len(keyboard.key_costs))]
    for (letter, key), assigned in keys_to_letters.items():
        if assigned.x == 1:
            key_assignments[key] = letter

    return KeyboardLayout(keyboard, key_assignments)


if __name__ == "__main__":
    keyboard = Keyboard.random()  # TODO
    letter_weights = LetterWeights.load()
    layout = find_optimal_layout(keyboard, letter_weights)
    print(repr(layout))

# Local Variables:
# compile-command: "sudo -u cat /home/cat/code/svalboard-opt/run.sh"
# End:
