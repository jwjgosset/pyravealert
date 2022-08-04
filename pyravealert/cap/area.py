"""
CAP v1.2
========

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import List, Optional

from .geocode import GeoCode


@dataclass
class Area:
    class Meta:
        name = "area"
        nillable = True

    areaDesc: str

    polygon: Optional[List[str]] = field(default=None)

    circle: Optional[List[str]] = field(default=None)

    geocode: Optional[List[GeoCode]] = field(default=None)

    altitude: Optional[float] = field(default=None)

    ceiling: Optional[float] = field(default=None)
