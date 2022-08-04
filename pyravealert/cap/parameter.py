"""
CAP v1.2
========

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass


@dataclass
class Parameter:
    class Meta:
        name = "parameter"
        nillable = True

    valueName: str

    value: str
