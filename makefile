test: tests.tmp

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__
	rm -f tests.tmp

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

models.html: models.py
	pydoc3 -w models

IDB2.log:
	git log > IDB2.log

tests.tmp: 
	python3 tests.py
	coverage3 run --source=tests.py,models.py --omit=*/sqlalchemy/* --branch tests.py >  tests.tmp 2>&1
	coverage3 report -m                      >> tests.tmp
	cat tests.tmp

pip3: python
	apt-get install python3-pip
	pip3 install flask
	pip3 install flask-compress
	pip3 install ijson
	pip3 install pyjade
	pip3 install PyMySQL
	pip3 install SQLAlchemy
	pip3 install pysolr
	pip3 install numpy
	pip3 install coverage

python:
	apt-get install -y python3

build: 
	grunt build imagemin

solr-start:
	sh solr/start.sh
	
index:
	~/solr2/bin/solr stop -all
	sudo rm -Rf ~/solr2/example/cloud/
	~/solr2/bin/solr start -e cloud -noprompt
	~/solr2/bin/post -c gettingstarted scripts/giantbomb/json/games.json
	~/solr2/bin/post -c gettingstarted scripts/giantbomb/json/platforms.json
	~/solr2/bin/post -c gettingstarted scripts/giantbomb/json/companies.json

start:
	sudo service mysql restart
	~/solr-5.3.1/bin/solr stop -all
	~/solr-5.3.1/bin/solr start -e cloud -noprompt
	python3 migrate.py
	sudo python3 index.py 
restart:
	pm2 restart index.py

stop:
	pm2 kill

install:
	sudo . scripts/setup/install.sh

increase_swap:
	dd if=/dev/zero of=/swapfile bs=1024 count=1024k
	fallocate -l 1G /mnt/1GB.swap
	mkswap /mnt/1GB.swap
	swapon /mnt/1GB.swap
	echo '/mnt/1GB.swap  none  swap  sw 0  0' >> /etc/fstab
	echo 'vm.swappiness=10' >> /etc/sysctl.conf

