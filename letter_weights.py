#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class LetterWeights:
    letters: dict[str, int]  # map from letter to frequency
    digraphs: dict[str, int]  # map from letter pair to frequency

    @staticmethod
    def load():
        raise NotImplementedError
