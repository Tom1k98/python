import argparse
import subprocess
from subprocess import PIPE
from datetime import datetime

atm = datetime.now()
TIME_STAMP = atm.strftime("%d%m%y%H%M")

def parseArgs():
	global args
	parser = argparse.ArgumentParser(description="tool for kvm vm backup")
	parser.add_argument('-n', '--name', nargs="+", help='virtual names separated by commas', required=True)
	args = parser.parse_args()

def execBackup(vmname):
    bc_name = f"{vmname}{TIME_STAMP}"
    return subprocess.run(['virsh', 'snapshot-create-as', '--domain', vmname, '--name', bc_name], stderr=PIPE, stdout=PIPE)

if __name__ == '__main__':
    parseArgs()
    for virt in args.name:
        execBackup(virt)
