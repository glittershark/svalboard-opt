#!/usr/bin/env python3

from dataclasses import dataclass

import os


@dataclass
class LetterWeights:
    letters: dict[str, int]  # map from letter to frequency
    digraphs: dict[str, int]  # map from letter pair to frequency
    trigraphs: dict[str, int]  # map from letter triplet to frequency

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
    ):

        l = LetterWeights()
        for p in [
            [l.letters, letters],
            [l.digraphs, digraphs],
            [l.trigraphs, trigraphs],
        ]:
            p[0] |= LetterWeights._ingest(os.path.join(directory, p[1]))

        return l

    @staticmethod
    def _ingest(path):
        contents = None
        with open(path, "r") as f:
            contents = f.read()

        ngraphs: dict[str, int] = {}

        for line in contents.splitlines():
            tokens = line.split(" ", maxsplit=1)
            ngraphs[tokens[1]] = int(tokens[0])

        return ngraphs
