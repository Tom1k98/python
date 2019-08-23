import psutil
import os
import socket
from datetime import datetime

host = socket.gethostname()
tmp = datetime.now()
now = tmp.strftime("%m%d%Y")
filename = '{}-{}'.format(host, now)
file = open(filename, 'w')
running = []

def getproc(name):
	for proc in psutil.process_iter():
		if proc.name() in name:
			running.append(name)

def genproc():
	procs = ['ansa_linux_x86_64', 'meta_post_x86_64', 'a4']
	for getp in procs:
		getproc(getp)



def selectproc():
	if 'a4' in running:
		animator = 'animator - {}'.format(host)
		file.write(animator)

	if 'ansa_linux_x86_64' in running:
		ansa = 'ansa - {}'.format(host)
		file.write(ansa)

	if 'meta_post_x86_64' in running:
		meta = 'meta - {}'.format(host)
		file.write(meta)

def main():

		genproc()
		selectproc()

if __name__ == "__main__":
	main()
