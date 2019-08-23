import psutil
import os
import socket

host = socket.gethostname()
running = []
ptime = []
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
		print(animator)

	if 'ansa_linux_x86_64' in running:
		ansa = 'ansa - {}'.format(host)
		print(ansa)

	if 'meta_post_x86_64' in running:
		meta = 'meta - {}'.format(host)
		print(meta)
		
def main():

		genproc()
		selectproc()

if __name__ == "__main__":
	main()
