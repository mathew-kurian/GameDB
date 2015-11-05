#!/usr/bin/env bash

# Tested on Ubuntu 14.10 Trusty Tar

apt-get update
apt-get -y upgrade

cd ~
apt-get -y install git
curl -L https://github.com/github/git-lfs/releases/download/v1.0.2/git-lfs-linux-amd64-1.0.2.tar.gz | tar -zx
cd git-lfs-1.0.2
./install.sh
cd ..

apt-get -y install python3
apt-get -y install python3-pip
pip3 install flask
pip3 install flask-compress
pip3 install ijson
pip3 install flask-cors
pip3 install pyjade
pip3 install PyMySQL
pip3 install SQLAlchemy
pip3 install numpy
pip3 install coverage

git clone https://github.com/bluejamesbond/cs373-idb
cd cs373-idb
git pull
git lfs pull
rm -rf node_modules

curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.29.0/install.sh | bash
source ~/.bashrc
source ~/.bash_profile
nvm install stable

npm install pm2 -g
npm install grunt-cli -g
npm install

grunt build
grunt imagemin

apt-get -y install ruby
gem install sass

apt-get -y install debconf-utils
debconf-set-selections <<< 'mysql-server mysql-server/root_password password 123456'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 123456'
apt-get -y install mysql-server

mysql -u root --password=123456 -e "create database IF NOT EXISTS idb CHARACTER SET = utf8mb4"

python3 migrate.py
pm2 start -i 1 -x --interpreter python3 index.py
pm2 restart index

grunt build