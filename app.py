"""
..  codeauthor:: Charles Blais
"""
import os

import logging

from typing import Optional, Dict

# Third-party library
from flask import Flask, jsonify, request

from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash

# User-contributed library
from pyravealert.config import get_app_settings, LogLevels

from pyoasiscap.cap import from_string, Alert

from pathlib import Path

import shutil

import traceback


settings = get_app_settings()

if os.getenv('FLASK_ENV') == 'development':
    settings.log_level = LogLevels.DEBUG
if os.getenv('FLASK_RUN_PORT'):
    settings.ws_port = int(os.environ['FLASK_RUN_PORT'])


class GeneralException(Exception):
    status_code = 500

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        payload: Optional[Dict] = None
    ):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['status_code'] = self.status_code
        rv['message'] = self.message
        return rv


class InvalidUsage(GeneralException):
    """Invalid usage exception"""
    status_code = 400


def _set_flask_logging():
    """
    Set the logging stream
    """
    settings = get_app_settings()
    settings.configure_logging()


def _validate_cap(alert: Alert):
    """
    We validate the message before accepting.  Key elements
    that need to exist or not.

    - Must contain a "---" with pre and post text
    - No line starting with
        - Insert a description
        - Insérez une description
    """
    if len(alert.info) == 0:
        raise InvalidUsage('No <info> element in the CAP alert')
    description = alert.info[0].description
    parts = description.split('---')
    if len(parts) != 2:
        raise InvalidUsage('Must be split by --- characters')
    if parts[0].startswith('Insert'):
        raise InvalidUsage('English not changed from default')
    if parts[1].startswith('Insérez'):
        raise InvalidUsage('French not changed from default')


def create_app():
    """Create flask API"""
    # Start the flask API
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    @auth.verify_password
    def verify_password(username: str, password: str) -> Optional[str]:
        settings = get_app_settings()
        if (
            username in settings.ws_basic_auth
            and
            check_password_hash(
                generate_password_hash(settings.ws_basic_auth[username]),
                password,
            )
        ):
            return username
        return None

    @app.route('/', methods=['POST'])
    @auth.login_required
    def post_cap():
        _set_flask_logging()

        settings = get_app_settings()

        # We attempt to parse to validate the content of the informat
        try:
            alert = from_string(request.get_data().decode('utf-8'))
        except Exception as err:
            logging.error(traceback.format_exc())
            raise GeneralException(str(err))

        logging.info(f'Received CAP alert: {alert}')

        # Before accepting the message, we make sure that key description
        # elements are in the file.
        _validate_cap(alert)

        directory = Path(settings.ws_write_directory)
        # Before writing the file, we make sure to mv all xml files in the
        # web service directory to an archive folder.
        archive = directory.joinpath('archive')
        archive.mkdir(mode=0o755, parents=True, exist_ok=True)
        for oldfile in directory.glob('*.xml'):
            logging.info(f'Moving {oldfile} to archive')
            shutil.move(
                oldfile,
                oldfile.parent.joinpath('archive', f'{oldfile.name}'))

        # We store the results in file using the identifier has reference
        filename = str(Path(
            settings.ws_write_directory
        ).joinpath(alert.identifier))
        logging.info(f'Writing result to {filename}')
        with open(filename, 'w') as fp:
            fp.write(request.get_data().decode('utf-8'))
            fp.close()

        return jsonify({
            'status_code': 200,
            'message': f'uploaded {alert.identifier}'
        })

    @app.errorhandler(GeneralException)
    def handle_error(
        error: GeneralException,
    ):
        """Return json response for invalid response"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=settings.ws_port)
