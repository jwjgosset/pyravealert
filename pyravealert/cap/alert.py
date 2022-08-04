"""
CAP v1.2
========

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional, List

import datetime

from enum import Enum

from .info import Info


class Status(Enum):
    actual = 'Actual'
    exercise = 'Exercise'
    system = 'System'
    test = 'Test'
    draft = 'Draft'


class MsgType(Enum):
    alert = 'Alert'
    update = 'Update'
    cancel = 'Cancel'
    ack = 'Ack'
    error = 'Error'


class Scope(Enum):
    public = 'Public'
    restricted = 'Restricted'
    private = 'Private'


@dataclass
class Alert:
    class Meta:
        name = "alert"
        nillable = True
        namespace = "urn:oasis:names:tc:emergency:cap:1.2"

    identifier: str

    sender: str

    sent: datetime.datetime = field(
        metadata=dict(format='%Y-%m-%dT%H:%M:%S+00:00'))

    status: Status

    msgType: MsgType

    scope: Scope

    source: Optional[str] = field(default=None)

    restriction: Optional[str] = field(default=None)

    addresses: Optional[str] = field(default=None)

    code: Optional[List[str]] = field(default=None)

    note: Optional[str] = field(default=None)

    references: Optional[str] = field(default=None)

    incidents: Optional[str] = field(default=None)

    info: List[Info] = field(default_factory=list)
