'''
.. codeauthor:: Charles Blais
'''
import logging

from click.testing import CliRunner

from requests_mock.mocker import Mocker

from pyravealert.config import get_app_settings

from pyravealert.bin import ravealert


def test_rave_cli(requests_mock: Mocker):
    settings = get_app_settings()

    requests_mock.post(settings.url)

    runner = CliRunner()
    result = runner.invoke(ravealert.main)

    logging.info(result.exception)

    assert result.exit_code == 0
    assert requests_mock.called_once
