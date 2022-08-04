"""
CAP v1.2
========

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass


@dataclass
class GeoCode:
    class Meta:
        name = "geocode"
        nillable = True

    valueName: str

    value: str
