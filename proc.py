import psutil
running = []
def getproc(name):
	for proc in psutil.process_iter():
		if proc.name() in name:
			running.append(name)

def main():
	procs = ['ansa_linux_x86_64', 'meta_post_x86_64']
	for getp in procs:
		getproc(getp)

	for p in running:
		print("proces {} bezi".format(p))

if __name__ == "__main__":
	main()
