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
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(archive)

    remove(archive_path)


if __name__ == "__main__":
    install()