import subprocess
import tarfile
from subprocess import PIPE
from datetime import datetime

PATH_IN = '/Users/tom'
PATH_OUT = ''

atm = datetime.now()
TIME_STAMP = atm.strftime("%d%m%y")

def findFiles(vmname):
    return subprocess.run(['find', PATH_IN, '-daystart', '-cstart', '0', '-print'], stderr=PIPE, stdout=PIPE)