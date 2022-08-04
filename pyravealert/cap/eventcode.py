"""
CAP v1.2
========

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass


@dataclass
class EventCode:
    class Meta:
        name = "eventCode"
        nillable = True

    valueName: str

    value: str
