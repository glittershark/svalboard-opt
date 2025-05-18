#!/usr/bin/env python3

import os

os.environ["GRB_LICENSE_FILE"] = f"{os.getcwd()}/gurobi.lic"
print(os.getenv("GRB_LICENSE_FILE"))

import gurobipy as gp
import pandas as pd
import numpy as np
from dataclasses import dataclass
import itertools
import collections

from letter_weights import LetterWeights


@dataclass
class KeyboardLayout:
    key_assignments: list[str]

    def assigned_letter(self, key):
        return self.key_assignments[letter]

    def assigned_key(self, letter):
        return self.key_assignments.index(letter)


letter_frequencies = pd.read_csv(
    "./letter-frequencies.csv",
    header=None,
    names=["letter", "texts", "dictionaries"],
    index_col="letter",
)

key_costs = np.abs(np.random.randn(26))

letters = [*letter_frequencies.index]
assert len(letters) == 26

keys = [*range(26)]

text = """
E 1277 TH 50 THE 89
T 855 ER 40 AND 54
O 807 ON 39 THA 47
A 778 AN 38 ENT 39
N 686 RE 36 ION 36
I 667 HE 33 TIO 33
R 651 IN 31 FOR 33
S 622 ED 30 NDE 31
H 595 ND 30 HAS 28
D 402 HA 26 NCE 27
L 372 AT 25 EDT 27
U 308 EN 25 TIS 25
C 296 ES 25
M 288 OF 25
P 223 OR 25
F 197 NT 24
Y 196
W 176
G 174
B 141
V 112
K 74
J 51
X 27
Z 17
Q 8
"""


letter_weights = collections.defaultdict(lambda: 0)
digraph_weights = collections.defaultdict(lambda: 0)
trigraph_weights = collections.defaultdict(lambda: 0)

for line in text.splitlines():
    if not line:
        continue

    for chunk, freq in itertools.batched(line.split(" "), 2):
        freq = int(freq)
        if len(chunk) == 1:
            letter_weights[chunk] = freq
        elif len(chunk) == 2:
            digraph_weights[chunk] = freq
        elif len(chunk) == 3:
            trigraph_weights[chunk] = freq
        else:
            raise "Wrong chunk length"

key_transfer_costs = np.abs(np.random.randn(26, 26))

digraphs = [*digraph_weights.keys()]

m = gp.Model()
keys_to_letters = m.addVars(letters, keys, vtype=gp.GRB.BINARY)

m.addConstrs(
    (sum(keys_to_letters[letter, key] for key in keys) == 1 for letter in letters),
    name="each letter assigned once",
)

m.addConstrs(
    (sum(keys_to_letters[letter, key] for letter in letters) == 1 for key in keys),
    name="each key assigned once",
)


def key_letter_weight(letter, key):
    return letter_weights[letter] * key_costs[key]


def digraph_weight(digraph, key_pair):
    return digraph_weights[digraph] * key_transfer_costs[key_pair]


m.setObjective(
    sum(
        key_letter_weight(letter, key) * keys_to_letters[letter, key]
        for letter in letters
        for key in keys
    )
    + sum(
        digraph_weight(digraph, (key1, key2))
        * keys_to_letters[digraph[0], key1]
        * keys_to_letters[digraph[1], key2]
        for digraph in digraphs
        for key1 in keys
        for key2 in keys
    ),
    sense=gp.GRB.MINIMIZE,
)

m.optimize()

key_assignments = [None for _ in range(len(key_costs))]
for (letter, key), assigned in keys_to_letters.items():
    if assigned.x == 1:
        key_assignments[key] = letter


layout = KeyboardLayout(key_assignments)

# Local Variables:
# compile-command: "sudo -u cat /home/cat/code/svalboard-opt/run.sh"
# End:
