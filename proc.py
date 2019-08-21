#!/usr/bin/python3
import psutil
for proc in psutil.process_iter():
    if proc.name() in "firefox":
        print("je tam")
