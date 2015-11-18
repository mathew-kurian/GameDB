#!/usr/bin/env python
import subprocess

p = subprocess.Popen("solr/start.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while p.poll() is None:
	print('None' if p.stdout is None else p.stdout.readline().decode("utf-8"))
	continue
