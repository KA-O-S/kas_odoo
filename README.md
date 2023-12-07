# odoo-docker

1. remove all .gitkeep Files in all empty Folder --> find . -name ".gitkeep" -exec rm {} \;
   Set PW for DB & odoo in odoo.conf
   - postgres/init/init.sql
   - MasterPW in /postgre/Dockerfile 
    Set odoo.conf
   - limit-memory-soft = 2048 X No of worker * 1024 * 1024 or default
   - limit-memory-hard = 2560 X No of worker * 1024 * 1024 or default
   
2. Set .htpasswd --> apt install apache2-utils --> on nginx/config --> htpasswd -c ./.htpasswd cakru-it

3. Build single container certbot 
For Hetzner
------------------ 
Exampel--> docker-compose run certbot certonly -n --agree-tos --email c.krumpholz@cakru-it.com --authenticator dns-hetzner --dns-hetzner-credentials /etc/letsencrypt/credentials.ini --dns-hetzner-propagation-seconds=60 -d 'cakru-it.de' -d '*.cakru-it.de'
------------------

For other DNS try !!!! --webroot !!!!!
------------------
Exampel--> docker-compose run certbot certonly --webroot --preferred-challenges dns -d 'cakru-it.de' -d '*.cakru-it.de'

For automatic renew copy service & timer build folder to systemd/system
chmod 644
systemctl enable certbot-renew.timer
systemctl start certbot-renew.timer

4. docker-compose up --build 
5. docker exec -it -u root odoo-live chown -R odoo:odoo var/lib/odoo
6. docker exec -it -u root odoo-stage chown -R odoo:odoo var/lib/odoo
7. nginx config for domain --> default.conf !!! also for ssl path!!!
