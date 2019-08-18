#!/usr/bin/python3
import sys 
import os 
print("coonect to:\n1. srv-245\n2. srv-208\n3. srv-018")
srv = int(input("select: "))
print(srv)
if srv not in range(1, 3):
    print("error")
    sys.exit()
else:
    if srv is 1:
        os.system("ssh storc@192.168.2.245")
    elif srv is 2:
        os.system("ssh storc@192.168.2.208")
    elif srv in 3:
        os.system("ssh storc@192.168.2.18")

