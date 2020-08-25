import subprocess
import tarfile
from subprocess import PIPE
from datetime import datetime

atm = datetime.now()
TIME_STAMP = atm.strftime("%d%m%y%H%M")

def findFiles(vmname):
    return subprocess.run(['find', 'snapshot-create-as', '--domain', vmname, '--name', bc_name], stderr=PIPE, stdout=PIPE)