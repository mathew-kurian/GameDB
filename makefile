clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__

config:
	git config -l

scrub:
	make clean
	rm -f  model.html
	rm -f  IDB1.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: tests.tmp

idb1-tests:
	git clone https://github.com/bluejamesbond/cs373-idb.git

models.html: models.py
	pydoc3 -w models

IDB1.log:
	git log > IDB1.log

tests.tmp: tests.py
	coverage3 run    --branch tests.py >  tests.tmp 2>&1
	coverage3 report -m                      >> tests.tmp
	cat tests.tmp