'''
..  codeauthor:: Charles Blais
'''
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .alert import Alert


def from_string(content: str) -> Alert:
    '''
    Parse from string
    '''
    parser = XmlParser()
    return parser.from_string(content, Alert)


def from_file(filename: str) -> Alert:
    '''
    Parse content from file
    '''
    parser = XmlParser()
    return parser.parse(filename, Alert)


def to_string(alert: Alert) -> str:
    '''
    Convert an event to string object
    '''
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    return serializer.render(
        alert,
        ns_map={None: "urn:oasis:names:tc:emergency:cap:1.2"})
