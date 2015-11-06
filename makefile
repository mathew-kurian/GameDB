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

idb2-tests:
	git clone https://github.com/bluejamesbond/cs373-idb.git

models.html: models.py
	pydoc3 -w models

IDB2.log:
	git log > IDB2.log

tests.tmp: tests.py
	coverage3 run --source=tests.py,models.py --omit=*/sqlalchemy/* --branch tests.py >  tests.tmp 2>&1
	coverage3 report -m                      >> tests.tmp
	cat tests.tmp

build: 
	sudo service mysql start
	python3 migrate.py

pip3: python
	apt-get install python3-pip
	pip3 install flask
	pip3 install flask-compress
	pip3 install ijson
	pip3 install flask-cors
	pip3 install pyjade
	pip3 install PyMySQL
	pip3 install SQLAlchemy
	pip3 install numpy
	pip3 install coverage

python:
	apt-get install -y python3

pm2:
	npm install pm2 -g

grunt-cli:
	npm install grunt-cli -g

ruby:
	apt-get -y install ruby
	gem install sass

server:
	apt-get -y install debconf-utils
	debconf-set-selections <<< 'mysql-server mysql-server/root_password password 123456'
	debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 123456'
	apt-get -y install mysql-server
	mysql -u root --password=123456 -e "create database IF NOT EXISTS idb CHARACTER SET = utf8mb4"

start-server:
	sudo service mysql start
	python3 migrate.py

stop-server:
	sudo service mysql stop

full_install:
	dd if=/dev/zero of=/swapfile bs=1024 count=1024k
	fallocate -l 1G /mnt/1GB.swap
	mkswap /mnt/1GB.swap
	swapon /mnt/1GB.swap
	echo '/mnt/1GB.swap  none  swap  sw 0  0' >> /etc/fstab
	echo 'vm.swappiness=10' >> /etc/sysctl.conf
	sudo scripts/setup/install.sh

install:
	sudo scripts/setup/install.sh

increase_swap:
	dd if=/dev/zero of=/swapfile bs=1024 count=1024k
	fallocate -l 1G /mnt/1GB.swap
	mkswap /mnt/1GB.swap
	swapon /mnt/1GB.swap
	echo '/mnt/1GB.swap  none  swap  sw 0  0' >> /etc/fstab
	echo 'vm.swappiness=10' >> /etc/sysctl.conf

