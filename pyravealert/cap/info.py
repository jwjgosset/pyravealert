"""
CAP v1.2
========

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional, List

from enum import Enum

from .eventcode import EventCode

from .parameter import Parameter

from .resource import Resource

from .area import Area


class Category(Enum):
    geo = "Geo"
    met = "Met"
    safety = "Safety"
    security = "Security"
    rescue = "Rescue"
    fire = "Fire"
    health = "Health"
    env = "Env"
    transport = "Transport"
    infra = "Infra"
    cbrne = "CBRNE"
    other = "Other"


class ResponseType(Enum):
    shelter = "Shelter"
    evacuate = "Evacuate"
    prepare = "Prepare"
    execute = "Execute"
    avoid = "Avoid"
    monitor = "Monitor"
    assess = "Assess"
    allclear = "AllClear"
    none = "None"


class Urgency(Enum):
    immediate = "Immediate"
    expected = "Expected"
    future = "Future"
    past = "Past"
    unknown = "Unknown"


class Severity(Enum):
    extreme = "Extreme"
    severe = "Severe"
    moderate = "Moderate"
    minor = "Minor"
    unknown = "Unknown"


class Certainty(Enum):
    observed = "Observed"
    likely = "Likely"
    possible = "Possible"
    unlikely = "Unlikely"
    unknown = "Unknown"


@dataclass
class Info:
    class Meta:
        name = "info"
        nillable = True

    language: str = 'en-US'

    category: List[Category] = field(default_factory=list)

    event: str = field(default='')

    responseType: Optional[List[ResponseType]] = field(default=None)

    urgency: Urgency = field(default=Urgency.unknown)

    severity: Severity = field(default=Severity.unknown)

    certainty: Certainty = field(default=Certainty.unknown)

    audience: Optional[str] = field(default=None)

    eventCode: List[EventCode] = field(default_factory=list)

    # important to note that format must be YYYY-mm-ddTHH:MM:SS+HH:MM
    # we have to use string since python datetime timezone offset doesn't
    # support HH:MM format
    effective: Optional[str] = field(default=None)

    onset: Optional[str] = field(default=None)

    expires: Optional[str] = field(default=None)

    senderName: Optional[str] = field(default=None)

    headline: Optional[str] = field(default=None)

    description: Optional[str] = field(default=None)

    instruction: Optional[str] = field(default=None)

    web: Optional[str] = field(default=None)

    contact: Optional[str] = field(default=None)

    parameter: Optional[List[Parameter]] = field(default=None)

    resource: Optional[List[Resource]] = field(default=None)

    area: Optional[List[Area]] = field(default=None)
