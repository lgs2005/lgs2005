'''Allows use of NodeJS and npm without access to sudo on linux systems.
This script is a direct substitute for npm, accepting the same arguments.
'''


import os
import sys
import tarfile

from urllib.request import urlretrieve

NODE_URL = 'https://nodejs.org/dist/v18.12.1/node-v18.12.1-linux-x64.tar.xz'
ARCHIVE_NAME = 'node-v18.12.1-linux-x64'

install_directory = './' + ARCHIVE_NAME
archive_path = './' + ARCHIVE_NAME + '.tar.xz'

def run():
    # move into correct working directory
    thisdir = os.path.dirname(__file__)
    if thisdir != '':
        os.chdir(thisdir)
    
    # install node if it doesnt exist
    if not os.path.exists(install_directory):
        urlretrieve(NODE_URL, archive_path)

        with tarfile.open(archive_path) as archive:
            archive.extractall()

        os.remove(archive_path)
    
    # update path and pass arguments to npm process
    os.environ['PATH'] = f'{thisdir}/{archive_path}/bin:' + os.environ['PATH']
    
    sysargs = list(sys.argv)
    sysargs[0] = f'{thisdir}/{archive_path}/bin/npm'
    
    os.system(' '.join(sysargs))


if __name__ == '__main__':
    run()