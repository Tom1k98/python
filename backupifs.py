import subprocess
import tarfile
from subprocess import PIPE
from datetime import datetime
import logging
import shutil
import sys

PATH_IN = '/oracle/FRA/PROD/backup'
PATH_OUT = '/mnt/IKOS-EXPORT/ifs_bc'
LOG_FILE = '/var/log/ifs_backup.log'

atm = datetime.now()
TIME_STAMP = atm.strftime("%d%m%y")


def findFiles():
   return subprocess.run(['find', PATH_IN, '-type', 'f', '-mtime', '-1', '-print'], stderr=PIPE, stdout=PIPE).stdout.decode('UTF-8').split('\n')

def makeTar(files):
    tar_name = f'{PATH_OUT}/ifsbc_{TIME_STAMP}.tar.gz'
    logging.info(f'creating new tar file {tar_name}')
    with tarfile.open(tar_name, 'w:gz') as tar:
        for file in files:
            logging.info(f'adding file {file} to {tar_name}')
            tar.add(file)
            logging.info(f'file {file} added successfully')

def enoughSpace():
    total, used, free = shutil.disk_usage('/mnt')
    return True if ((free // 2**30) > 15) else False


if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
    isSpace = enoughSpace()
    if isSpace:
        files = findFiles()
        del files[-1]
        logging.info('files saved to list')
        makeTar(files)
        logging.info('tar created')
    else:
        logging.error('not enough space on disk, exiting')
        sys.exit()
    