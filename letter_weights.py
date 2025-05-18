#!/usr/bin/env python3

from dataclasses import dataclass, field

import os
import re


@dataclass
class LetterWeights:
    # map from letter to frequency
    letters: dict[str, int] = field(default_factory=dict)
    # map from letter pair to frequency
    digraphs: dict[str, int] = field(default_factory=dict)
    # map from letter triplet to frequency
    trigraphs: dict[str, int] = field(default_factory=dict)

    def __init__(self):
        self.letters = {}
        self.digraphs = {}
        self.trigraphs = {}

    @staticmethod
    def load(
        directory="./ngrams/eng_wiki_1m/",
        letters="1-grams.txt",
        digraphs="2-grams.txt",
        trigraphs="3-grams.txt",
        regex="[a-z ]+",
    ):
        ex = re.compile(regex)

        l = LetterWeights()
        for p in [
            [l.letters, letters],
            [l.digraphs, digraphs],
            [l.trigraphs, trigraphs],
        ]:
            p[0] |= LetterWeights._ingest(os.path.join(directory, p[1]), ex)

        return l

    @staticmethod
    def _ingest(path: str, ex: re.Pattern):
        contents = None
        with open(path, "r") as f:
            contents = f.read()

        ngraphs: dict[str, int] = {}

        for line in contents.splitlines():
            tokens = line.split(" ", maxsplit=1)
            graph = tokens[1]
            freq = int(tokens[0])
            if ex.fullmatch(graph):
                ngraphs[graph] = freq

        return ngraphs

    def all_letters(self) -> list[str]:
        return [*self.letters.keys()]

    def all_digraphs(self) -> list[str]:
        return [*self.digraphs.keys()]

    def top_k_digraphs(self, k) -> list[str]:
        return sorted(self.digraphs.keys(), key=lambda d: self.digraphs[d])
