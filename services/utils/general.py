"""Services for general utils"""

# Os
import os

def is_windows():
    if os.name == 'nt':
        return True
    return False


def rmfile(path):
    """Delete files from a path

    :param path: Path of the folder with files to will delete
    """
    os.remove(path)