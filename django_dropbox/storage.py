import os
import itertools

from dropbox.client import DropboxClient
from dropbox.session import DropboxSession
from dropbox.rest import ErrorResponse

from django.core.cache import cache
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.encoding import filepath_to_uri, force_text

from .compat import getFile, deconstructible

from .settings import (CONSUMER_KEY,
                       CONSUMER_SECRET,
                       ACCESS_TYPE,
                       ACCESS_TOKEN,
                       ACCESS_TOKEN_SECRET,
                       CACHE_TIMEOUT)


@deconstructible
class DropboxStorage(Storage):
    """A storage class providing access to resources in a Dropbox Public folder."""

    def __init__(self, location='/Public'):
        session = DropboxSession(
            CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TYPE, locale=None
        )
        session.set_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.client = DropboxClient(session)
        self.account_info = self.client.account_info()
        self.location = location
        self.base_url = 'http://dl.dropbox.com/u/{uid}/'.format(**self.account_info)

    def _get_abs_path(self, name):
        # the path to save in dropbox
        name = os.path.join(self.location, name)
        name = os.path.normpath(name)
        return force_text(name.replace('\\', '/'))

    def _open(self, name, mode='rb'):
        name = self._get_abs_path(name)
        remote_file = DropboxFile(name, self, mode=mode)
        return remote_file

    def _save(self, name, content):
        name = self._get_abs_path(name)
        directory = os.path.dirname(name)
        if not self.exists(directory) and directory:
            self.client.file_create_folder(directory)
        response = self.client.metadata(directory)
        if not response['is_dir']:
            raise IOError("%s exists and is not a directory." % directory)
        self.client.put_file(name, content)
        return name

    def delete(self, name):
        if name == '':
            return
        name = self._get_abs_path(name)
        if self.exists(name):
            self.client.file_delete(name)

    def exists(self, name):
        name = self._get_abs_path(name)
        try:
            metadata = self.client.metadata(name)
            if metadata.get('is_deleted'):
                return False
        except ErrorResponse as e:
            if e.status == 404:
                # not found
                return False
            raise e
        return True

    def listdir(self, path):
        path = self._get_abs_path(path)
        response = self.client.metadata(path)
        directories = []
        files = []
        for entry in response.get('contents', []):
            if entry['is_dir']:
                directories.append(os.path.basename(entry['path']))
            else:
                files.append(os.path.basename(entry['path']))
        return directories, files

    def size(self, name):
        cache_key = 'django-dropbox-size:%s' % filepath_to_uri(name)
        size = cache.get(cache_key)

        if not size:
            size = self.client.metadata(filepath_to_uri(name))['bytes']
            cache.set(cache_key, size, CACHE_TIMEOUT)

        return size

    def url(self, name):
        cache_key = 'django-dropbox-url:%s' % filepath_to_uri(name)
        url = cache.get(cache_key)

        if not url:
            url = self.client.share(
                filepath_to_uri(name), short_url=False
            )['url']
            # this replace is for force to dropbox url to send the url like
            # a content and don't like a link to download
            url = url.replace("www", "photos-4")

            cache.set(cache_key, url, CACHE_TIMEOUT)

        return url

    def get_available_name(self, name):
        """Return a filename that's free on the target storage system.
        available for new content to be written to."""
        name = self._get_abs_path(name)
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        # If the filename already exists add an underscore and a number (before
        # the file extension, if exists) to the filename until the generated
        # filename doesn't exist.
        count = itertools.count(1)
        while self.exists(name):
            # file_ext includes the dot.
            name = os.path.join(
                dir_name, "%s_%s%s" % (file_root, next(count), file_ext)
            )

        return name


class DropboxFile(File):
    def __init__(self, name, storage, mode):
        self._name = name
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self.file = getFile()
        self._is_read = False

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        if not self._is_read:
            self.file = self._storage.client.get_file(self._name)
            self._is_read = True
        return self.file.read(num_bytes)

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file = getFile(content)
        self._is_dirty = True
        self._is_read = True

    def close(self):
        if self._is_dirty:
            self._storage.client.put_file(self._name, self.file.getvalue())
        self.file.close()
