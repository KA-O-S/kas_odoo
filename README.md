# odoo-docker

1. remove all .gitkeep Files in all empty Folder --> find . -name ".gitkeep" -exec rm {} \;
   change PW for DB & odoo in odoo.conf
   
2. Set .htpasswd --> apt install apache2-utils --> on nginx/config --> htpasswd -c ./.htpasswd cakru-it 
3. build single container certbot 


For Hetzner
------------------ 
Exampel--> docker-compose run certbot certonly -n --agree-tos --email c.krumpholz@cakru-it.com --authenticator dns-hetzner --dns-hetzner-credentials /etc/letsencrypt/credentials.ini --dns-hetzner-propagation-seconds=60 -d 'motex.cakru-it.de'
------------------
For other DNS !!!! --manuel !!!!!
------------------
Exampel--> docker-compose run certbot certonly --manual --preferred-challenges dns -d 'dancingismagic.de' -d '*.dancingismagic.de'
4. docker-compose up --build 
5. docker exec -it -u root odoo-live chown -R odoo:odoo var/lib/odoo
6. docker exec -it -u root odoo-stage chown -R odoo:odoo var/lib/odoo
7. nginx config for domain --> default.conf !!! also for ssl path!!!
