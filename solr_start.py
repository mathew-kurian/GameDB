import subprocess

p = subprocess.Popen("make solr-start", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while p.poll() is None:
	continue