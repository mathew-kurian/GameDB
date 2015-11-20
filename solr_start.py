#!/usr/bin/env python
import subprocess

#this script serves to start solr by creating a subprocess that runs the start script
p = subprocess.Popen("solr/start.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#loops until process completes, while printing the output during each iteration
while p.poll() is None:
	print('None' if p.stdout is None else p.stdout.readline().decode("utf-8"))
	continue
