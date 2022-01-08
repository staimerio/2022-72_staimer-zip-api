"""Services for novels controller"""

# Retic
from retic import env, App as app

# Requests
import requests

# Os
import os

# Uuid
import uuid

# Services
from retic.services.responses import success_response, error_response
from services.utils.general import is_windows
from services.sendfiles import sendfiles
from services.utils.general import rmfile

FILES_MAX_SIZE = app.config.get('FILES_MAX_SIZE')


class Zip(object):

    def __init__(self):
        """Set the variables"""
        self.files_path = "{0}/public/files".format(
            os.getcwd()) if is_windows() else "public/files"
        self.uuid = uuid.uuid1().hex
        self.max_size = FILES_MAX_SIZE


def get_instance():
    """Get an Wikipedia instance from a language"""
    return Zip()


def create_folder(instance):
    _path = "{0}/{1}".format(instance.files_path, instance.uuid)
    _cmd = f'mkdir "{_path}"'
    _folder = os.system(_cmd)
    return _path


def get_images(instance, images_url):
    _images_folder = create_folder(instance)
    _count = 1
    for _image_url in images_url:
        _request = requests.get(_image_url, stream=True)
        if _request.status_code == 200:
            _image_file = "{0}.jpg".format(_count)
            _image_path = "{0}/{1}".format(_images_folder, _image_file)
            open(_image_path, 'wb').write(_request.content)
            _count+=1
    
    return {
        'images_folder': _images_folder,
    }


def download_torrent(instance, torrent, tool="transmission-cli"):
    _cmd = ""
    if tool == "transmission-cli":
        _cmd = 'transmission-cli "{0}" -f "echo a > /dev/null" -w "{1}"'.format(
            torrent['torrent_path'],
            torrent['torrent_folder'],
        )
    elif tool == "aria2c":
        _cmd = 'aria2c -T "{0}" --seed-time=0 --dir="{1}"'.format(
            torrent['torrent_path'],
            torrent['torrent_folder'],
        )
    else:
        _cmd = "{0} -s '{1}' -e 0 '{2}'".format(
            instance.ctorrent_path,
            torrent['torrent_folder'],
            torrent['torrent_path']
        )
    print(_cmd)
    os.system(f"{_cmd}")


def zip_images(instance, images, filename):
    _cmd = f"cd '{images['images_folder']}' && zip -r -s {instance.max_size} '{filename}.zip' *"
    print(_cmd)
    # -s {self.partes}
    os.system(_cmd)
    _files_delete = [_ for _ in os.listdir(
        f"{images['images_folder']}") if ".z" not in _]
    for _file in _files_delete:
        _cmd = 'rm -r "{0}/{1}"'.format(
            images['images_folder'],
            _file
        )
        print(_cmd)
        os.system(_cmd)


def get_content_from_file(fname):
    """Get all content from a file

    :param fname: Name of the file to get information.
    """

    """Open the file"""
    _book = open(fname, "rb")
    """Read the book"""
    _content = _book.read()
    """Close the file"""
    _book.close()
    """Return data"""
    return _content


def upload_files(instance, images, description_upload, credential):
    _files = []
    _info = None
    print(os.listdir(f"{images['images_folder']}"))
    for _file in os.listdir(f"{images['images_folder']}"):
        _filename = "{0}/{1}".format(images['images_folder'], _file)
        _binary_file = get_content_from_file(
            _filename)
        """Upload to drive server"""
        _files_to_upload = [
            ('files', (_file, _binary_file))
        ]
        _upload_file = sendfiles.upload_files(
            files=_files_to_upload,
            description=description_upload,
            credential=credential,
            parent=instance.uuid,
        )
        if _upload_file:
            if not _info:
                _info = {
                    u"description": _upload_file['data']['description'],
                    u"credential": _upload_file['data']['credential'],
                    u"folder": _upload_file['data']['folder'],
                    u"platform": _upload_file['data']['platform'],
                    u"code": _upload_file['data']['code'],
                }
            _files += _upload_file['data']['success']

        rmfile(_filename)
    _data_response = {
        **(_info if _info else {}),
        u'items': _files
    }

    return _data_response


def zip_remote_images(images_url, description_upload, credential, filename):
    instance = get_instance()
    _images = get_images(instance, images_url)
    _zip = zip_images(instance, _images, filename)
    _result = upload_files(instance, _images, description_upload, credential)

    return success_response(
        data=_result
    )
