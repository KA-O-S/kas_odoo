# odoo-docker

1. remove all .gitkeep Files in all empty Folder --> find . -name ".gitkeep" -exec rm {} \;
   change PW for DB & odoo in odoo.conf
2. Set .htpasswd --> apt install apache2-utils --> on nginx/config --> htpasswd -c ./.htpasswd cakru-it 
3. build single container certbot 
   --> docker-compose --build certbot certonly --manual --preferred-challenges=dns --manual-auth-hook /usr/local/bin/certbot-hetzner-auth.sh --manual-cleanup-hook /usr/local/bin/certbot-hetzner-cleanup.sh -d <example.com> -d *.<example.com>
4. docker-compose up --build 
5. docker exec -it -u root odoo-live chmod -R odoo:odoo var/lib/odoo
6. docker exec -it -u root odoo-stage chmod -R odoo:odoo var/lib/odoo
