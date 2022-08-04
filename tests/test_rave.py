'''
..  codeauthor:: Charles Blais
'''

from requests_mock.mocker import Mocker

from pyravealert.inbound import generate, send

from pyravealert.config import get_app_settings


def test_generate():
    alert = generate(headline='Testing')
    print(alert)
    assert alert.info[0].headline == 'Testing'


def test_send(requests_mock: Mocker):
    settings = get_app_settings()

    requests_mock.post(settings.url)

    if settings.username is None or settings.password is None:
        raise Exception('username/password not set')

    alert = generate(headline='Testing')
    send(
        alert,
        settings.url,
        settings.username,
        settings.password
    )

    assert requests_mock.called_once
    print(requests_mock.request_history[0].text)
    assert '<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">' \
        in requests_mock.request_history[0].text
