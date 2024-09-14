from __future__ import annotations

from dataclasses import dataclass
from re import Pattern
import re


@dataclass
class Outer:
    test: Pattern
    innert_test: Outer.Pattern

    class Pattern:
        def __init__(self, input: str):
            print(f"Inner class got {input}")


pattern = re.compile(".")

outer = Outer(test=pattern, innert_test=Outer.Pattern("test"))
