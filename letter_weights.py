#!/usr/bin/env python3

from dataclasses import dataclass

import os
import re


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
