from os import path, makedirs, remove
from urllib.request import urlretrieve
import tarfile

NODE_16_URL = "https://nodejs.org/dist/v16.16.0/node-v16.16.0-linux-x64.tar.xz"
ARCHIVE_NAME = "node-v16.16.0-linux-x64"

this_dir = path.dirname(__name__)
install_path = path.join(this_dir, ARCHIVE_NAME)
archive_path = path.join(this_dir, 'node16.tar.xz')

def install():
    if path.isdir(install_path):
        remove(install_path)

    urlretrieve(NODE_16_URL, archive_path)

    with tarfile.open(archive_path) as archive:
        archive.extractall()

    remove(archive_path)


if __name__ == "__main__":
    install()