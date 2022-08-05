'''
..  codeauthor:: Charles Blais
'''
import logging

from typing import List, Optional

import click

from pyravealert import inbound

from pyoasiscap.cap import to_string, from_file

from pyoasiscap.parameter import Parameter

from pyoasiscap.alert import Status, Scope

from pyoasiscap.info import ResponseType, Category

from pyravealert.config import get_app_settings, LogLevels


settings = get_app_settings()


@click.command()
@click.option(
    '--url',
    default=settings.url,
    help='Rave Alert CAP Inbound URL'
)
@click.option(
    '--username',
    default=settings.username,
)
@click.option(
    '--password',
    default=settings.password,
)
@click.option(
    '--file',
    type=click.Path(exists=True),
    help='Get CAP content from file',
)
@click.option(
    '-e', '--event',
    help='Event title of the message',
)
@click.option(
    '-H', '--headline',
    help='Headline of the message',
)
@click.option(
    '-d', '--description',
    help='Description of the message',
)
@click.option(
    '-i', '--instruction',
    help='Instruction of the message',
)
@click.option(
    '-w', '--web',
    help='Web link of the message',
)
@click.option(
    '-c', '--contact',
    help='Contact of the message',
)
@click.option(
    '-s', '--status',
    type=click.Choice([v.value for v in Status]),
    default='Test',
    help='Status'
)
@click.option(
    '-S', '--scope',
    type=click.Choice([v.value for v in Scope]),
    default='Private',
    help='Scope'
)
@click.option(
    '-l', '--language',
    default='en-CA',
    help='Language of the message (used only for identifier with Rave)',
)
@click.option(
    '-c', '--category',
    type=click.Choice([v.value for v in Category]),
    multiple=True,
    default=['Geo'],
    help='Category',
)
@click.option(
    '-r', '--response-type',
    type=click.Choice([v.value for v in ResponseType]),
    multiple=True,
    default=['None'],
    help='Response Type',
)
@click.option(
    '-p', '--parameter',
    multiple=True,
    help='Parameter by using = to divide value name and value'
)
@click.option(
    '--stdout-only',
    is_flag=True,
    help='stdout only output (do not send)'
)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help='Verbosity'
)
def main(
    url: str,
    username: str,
    password: str,
    file: Optional[str],
    event: Optional[str],
    headline: Optional[str],
    description: Optional[str],
    instruction: Optional[str],
    web: Optional[str],
    contact: Optional[str],
    status: str,
    scope: str,
    language: str,
    category: List[str],
    response_type: List[str],
    parameter: List[str],
    stdout_only: bool,
    log_level: str,
):
    '''
    Send simple message with headline to Rave Alert for quick messaging.

    NOTE: It is important to note that this is just a quick wrapper for
    simplified messaging.  It is recommended to use pyravealert library
    in any code instead of this function for full functionality.

    This is used by legacy systems for simple messaging.  It assumes
    constant conditions for certain CAP fields.  Those fields are:

        code = empty
        incidents = empty
        identifier = hostname-timestamp-language
        category = [Category.geo]
        urgency = Urgency.immediate
        certainty = Certainty.observed
        severity = Severity.severe
        eventCode = empty
        areaDesc = empty
        geocode = empty

    '''
    if log_level is not None:
        settings.log_level = LogLevels(log_level)
    if username is not None:
        settings.username = username
    if password is not None:
        settings.password = password
    settings.configure_logging()

    params = []
    for param in parameter:
        parts = param.split('=')
        if len(parts) != 2:
            raise ValueError(f'Invalid parameter format {param}')
        params.append(Parameter(
            valueName=parts[0], value=parts[1]
        ))

    if file is None:
        if event is None:
            raise ValueError('username/password not set')
        cap = inbound.generate(
            status=Status(status),
            scope=Scope(scope),
            event=event,
            language=language,
            category=[Category(c) for c in category],
            responseType=[ResponseType(r) for r in response_type],
            headline=headline,
            description=description,
            instruction=instruction,
            web=web,
            contact=contact,
            parameter=params,
        )
    else:
        cap = from_file(file)

    logging.debug(f'Generated CAP content: {cap}')

    if stdout_only:
        print(to_string(cap))
    else:
        if settings.username is None or settings.password is None:
            raise ValueError('username/password not set')
        inbound.send(
            cap,
            url,
            username,
            password
        )
