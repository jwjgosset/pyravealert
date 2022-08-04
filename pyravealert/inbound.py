'''
Rave message handler
====================

The following are quick notes from their documentation.

    - There can only be one info block per CAP message
    - There can only be one area block per CAP message
    - The following fields have the following props:

    identifier = must be unique per CAP listener
    msgType = only alert, cancel supported (atom only alert)
    code = can be used for CAP Inbound Rule
    headline, description, instruction, web, contact = cond mapped based on
        the output format
    parameter = can be used for CAP Inbound rule
    urgency, certainty, severity, status, category, responseType, scope = can
        be used for CAP inbound rule
    event = can be used for CAP Inbound rule
    geocode = can be used for CAP Inbound role


The mapping of text fields are as followed:

SMS = event, headline
email = incidents, headline, description, instruction, web, contact
voice = incidents, event, headline, description, instruction, contact
rss = incidents, event, headline, description, instruction, web, contact
twitter = event, headline

..  codeauthor:: Charles Blais
'''
import logging

import random

import string

from typing import Optional, List

import datetime

import socket

import requests

from requests.auth import HTTPBasicAuth

from .cap import to_string

from .cap.alert import Alert, Status, MsgType, Scope

from .cap.info import Info, Category, \
    ResponseType, Urgency, Certainty, Severity, EventCode, \
    Parameter, Area

from .cap.geocode import GeoCode


def generate(
    status: Status = Status.test,
    scope: Scope = Scope.private,
    code: List[str] = [],
    incidents: Optional[str] = None,
    identifier: Optional[str] = None,
    language: str = 'en-CA',
    event: str = 'CHIS Rave Alert Mobile message',
    category: List[Category] = [Category.geo],
    responseType: List[ResponseType] = [ResponseType.none],
    urgency: Urgency = Urgency.immediate,
    certainty: Certainty = Certainty.observed,
    severity: Severity = Severity.severe,
    eventCode: List[EventCode] = [],
    headline: Optional[str] = None,
    description: Optional[str] = None,
    instruction: Optional[str] = None,
    web: Optional[str] = None,
    contact: Optional[str] = None,
    parameter: List[Parameter] = [],
    areaDesc: Optional[str] = None,
    geocode: List[GeoCode] = [],
) -> Alert:
    '''
    Generate a Rave Alert cap message using a simplified form
    of arguments.

    .. note:: This quick method only support Alert msgType
    '''
    if identifier is None:
        identifier = f'{socket.gethostname()}-\
{datetime.datetime.utcnow().timestamp()}-\
{"".join(random.choice(string.ascii_lowercase) for i in range(5))}'

    area = [Area(areaDesc=areaDesc, geocode=geocode)] \
        if areaDesc is not None else None

    return Alert(
        identifier=identifier,
        status=status,
        msgType=MsgType.alert,
        scope=scope,
        code=code,
        incidents=incidents,
        # Required but not used
        sender=socket.gethostname(),
        sent=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
        info=[Info(
            category=category,
            event=event,
            responseType=responseType,
            urgency=urgency,
            certainty=certainty,
            severity=severity,
            eventCode=eventCode,
            headline=headline,
            description=description,
            instruction=instruction,
            web=web,
            contact=contact,
            parameter=parameter,
            area=area,
            # We set but not used
            language=language,
        )]
    )


def send(alert: Alert, url: str, username: str, password: str):
    '''
    Send CAP alert message to inbound CAP listener
    '''
    data = to_string(alert)
    logging.info(f'Sending CAP to Rave:\n{data}')

    req = requests.post(
        url,
        data=data,
        headers={
            'Content-Type': 'application/xml'
        },
        auth=HTTPBasicAuth(username, password)
    )
    req.raise_for_status()
