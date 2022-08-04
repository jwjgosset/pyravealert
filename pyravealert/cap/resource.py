"""
CAP v1.2
========

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional


@dataclass
class Resource:
    class Meta:
        name = "resource"
        nillable = True

    resourceDesc: str

    mimeType: str

    size: Optional[int] = field(default=None)

    uri: Optional[str] = field(default=None)

    derefUri: Optional[str] = field(default=None)

    digest: Optional[str] = field(default=None)
