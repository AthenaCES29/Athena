#!/bin/bash
echo "Instalação Python + Django + Postgresql"

# Python
apt-get install python2.7

# Git
apt-get install git

# Athena
apt-get install zip unzip
git clone https://github.com/ftuyama/Athena.git
chmod -R 777 Athena.sh

# pip
python get-pip.py
pip install -U pip
pip install -r requirements.txt

# virtualenv
apt-get install python-virtualenv
virtualenv /projectEnv

# Django
source /projectEnv/bin/activate
pip install django

# PostgreSQL
deactivate
apt-get install libpq-dev python-dev
apt-get install postgresql postgresql-contrib

# PGAdmin IIIcr
apt-get install pgadmin3
pip install django psycopg2

# Configure Database
echo "Talvez essa parte tenha de ser executada manualmente"
sudo -u postgres createuser --superuser postgres
sudo -u postgres psql
# Especialmente essa, para definir a senha...
\password postgres

sudo su - postgres
psql
CREATE DATABASE postgres;
CREATE USER postgres WITH PASSWORD '123';
GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;
pgadmin3


