import subprocess

p = subprocess.Popen("make solr-start", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while p.poll() is None:
	continue

print('STDOUT')
if p.stdout is None:
	print('-')
else:
	for line in p.stdout:
		print(line.decode("utf-8"), end = "")

print('\nSTDERR')
if p.stderr is None:
	print('-')
else:
	for line in p.stderr:
		print(line.decode("utf-8"), end = "")

print('\n')