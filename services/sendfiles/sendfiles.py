# Retic
from retic import env, App as app

# Requests
import requests

# Binascii
import binascii

# Constants
URL_FILES = app.apps['backend']['sendfiles']['base_url'] + \
    app.apps['backend']['sendfiles']['files']


def upload_files(files, description, credential=None, parent=None):
    """Upload a list of files to storage

    :param files: List of files to upload
    :param description: Description of the upload
    """

    """Prepare the payload"""
    _payload = {
        u"description": description,
        u"credential": credential,
        u"parent": parent,
    }

    """Build epub file"""
    _files = requests.post(
        URL_FILES,
        files=files,
        data=_payload
    )
    """Check if the response is valid"""
    if _files.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception(_files.text)
    """Get json response"""
    _files_json = _files.json()
    """Return data"""
    return _files_json
