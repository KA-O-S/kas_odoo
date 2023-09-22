#!/bin/bash

# USAGE: /bin/bash stage.sh (--upgrade)

db="STAGE_$(date '+%Y%m%d%H%M%S')"
from=$(grep 'FROM' /home/docker/build/.env | cut -d '=' -f2)
#version=$(grep 'VERSION' /home/docker/build/.env | cut -d '=' -f2)

# Check if source database is specified
if [ -z $from ]; then
    echo "FROM is undefined. Please set value in .env file."
    exit 1
fi

# Check if odoo version is specified
#if [ -z $version ]; then
#    echo "VERSION is undefined. Please set value in .env file."
#    exit 1
#fi

# get current database
current=$(grep 'db_name =' /home/docker/odoo/stage/config/odoo.conf | cut -d '=' -f2)

# Check if source database exists
if ! docker exec db psql -U postgres -lqt | cut -d \| -f 1 | grep -qw ${from}; then
    echo "Database ${from} does not exist. Please set value in .env file."
    exit 1
fi

# Check if destination database user exists
if ! docker exec db psql -U postgres -t -c '\du' | cut -d \| -f 1 | grep -qw "odoo_stage"; then
    echo "User odoo_stage does not exist."
    exit 1
fi

# Check if source filestore exists
if [ ! -d "/home/docker/odoo/live/volumes/data/filestore/${from}" ]; then
    echo "Filestore for database $from does not exist."
    exit 1
fi

# Dump Database
echo 'Dump Database ..'
docker exec db sh -c "pg_dump -U postgres -Fc ${from} > /home/backups/${from}.dump"

# Stop Odoo
echo 'Stop Odoo ..'
cd /home/docker && docker compose stop odoo-stage

# Copy Database
echo 'Copy Database ..'
docker exec db createdb -U odoo_stage -T template0 ${db}
docker exec db pg_restore --clean --if-exists --no-acl --no-owner -d ${db} -U odoo_stage /home/backups/${from}.dump

# Remove Dump
echo 'Remove Dump from Postgres Container ..'
docker exec db rm /home/backups/${from}.dump

# Check if database was not successfully created
if ! docker exec db psql -U postgres -lqt | cut -d \| -f 1 | grep -qw $db; then
    echo "Something went wrong. Database $db does not exist."
    exit 1;
fi

# Prepare Database
echo 'Prepare Database ..'

# Delete Mailserver (Incoming and Outgoing)
docker exec db psql -d ${db} -U odoo_stage -c "DELETE FROM fetchmail_server; DELETE FROM ir_mail_server;"

# Disable Crons
docker exec db psql -d ${db} -U odoo_stage -c "UPDATE ir_cron SET active = FALSE;"

# Set right Report Url (because there are some issues when odoo is behind htaccess)
docker exec db psql -d ${db} -U odoo_stage -c "DELETE FROM ir_config_parameter WHERE key = 'report.url'; INSERT INTO ir_config_parameter (value, key) VALUES ('http://0.0.0.0:9069', 'report.url');"

# Delete Enterprise Code
docker exec db psql -d ${db} -U odoo_stage -c "DELETE FROM ir_config_parameter WHERE key = 'mail.bounce.alias';"

# Change UUID of Database
docker exec db psql -d ${db} -U odoo_stage -c "UPDATE ir_config_parameter SET value = '"$(uuidgen)"' WHERE key = 'database.uuid';"

# Copy Filestore
echo 'Copy Filestore ..'
mkdir -p /home/docker/odoo/stage/volumes/data/filestore/${db}
cp -a /home/docker/odoo/live/volumes/data/filestore/${from}/. /home/docker/odoo/stage/volumes/data/filestore/${db}

# Change Database Name in Odoo Config
echo 'Change Databasename in Config ..'
sed -i "s/$(sed -n '/db_name/p' /home/docker/odoo/stage/config/odoo.conf)/db_name = ${db}/g" /home/docker/odoo/stage/config/odoo.conf

# Do not show database manager
sed -i "s/$(sed -n '/list_db/p' /home/docker/odoo/stage/config/odoo.conf)/list_db = False/g" /home/docker/odoo/stage/config/odoo.conf

# Do a full update
if [ "$1" == "--upgrade" ]; then
    echo 'Update Database ..'
    cd /home/docker && docker compose run --rm odoo-stage /home/odoo/addons/odoo/odoo-bin -u all --stop-after-init -d ${db} -c /etc/odoo/odoo.conf
fi

# Delete old databases
if [ -z $current ]; then
    current=$db
fi

databases=$(docker exec db psql -U postgres -lqt | cut -d \| -f 1 | grep -Fv -e $current -e $db | grep "STAGE")
for i in ${databases}; do

    if [ -d "/home/docker/odoo/stage/volumes/data/filestore/${i}" ]; then

        rm -r /home/docker/odoo/stage/volumes/data/filestore/${i}

    fi

    if docker exec db psql -U postgres -lqt | cut -d \| -f 1 | grep -qw $i; then

        docker exec db psql -U postgres -o /dev/null -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = '${i}';"

        docker exec db dropdb -U postgres ${i}

    fi

done

# Start Odoo
echo 'Start Odoo ..'
cd /home/docker && docker compose start odoo-stage

# Finish
echo "Created new Database (${db})."
exit 0
