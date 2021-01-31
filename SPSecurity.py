import hashlib
import sys


LICENSE_ERROR = PermissionError("You do not have a license key !")


def checksum(path: str, algorithm: callable = hashlib.md5):
    """
    Get checksum file signature
    :param path: str
    :param algorithm: callable
    :return: str, exception
    """

    algorithm = algorithm()

    try:
        with open(path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                algorithm.update(chunk)

        return algorithm.hexdigest(), None

    except Exception as error:
        return '', error


def secure_string(value: [bytes, tuple]):
    """
    :param value: bytes or tuple
    :return: tuple or bytes
    """

    if isinstance(value, bytes):
        return tuple(value)

    elif isinstance(value, tuple):
        return bytes(value)


class AntiDebugger:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def check(self):
        parent = self._kwargs.get('parent', '').lower()
        parents = self._kwargs.get('parents', [])

        if any(parent == i.lower() for i in parents):
            return None

        sys.exit()


class License:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def check(self):
        """
        :exception LICENSE_ERROR
        """

        _path = self._kwargs.get('path', ())
        _checksum = self._kwargs.get('checksum', ())

        if _path and _checksum:
            _currentChecksum, _ = checksum(secure_string(_path).decode())

            if secure_string(_checksum).decode() == _currentChecksum:
                return None

        raise LICENSE_ERROR
