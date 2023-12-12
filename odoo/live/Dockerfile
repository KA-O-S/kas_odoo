from odoo:16.0
USER root
COPY /home/odoo-docker/odoo_17.0+e.latest_all.deb /tmp/
RUN dpkg -i /tmp/odoo_17.0+e.latest_all.deb
RUN cd /var/lib && chown -R odoo:odoo odoo
# Expose Odoo services
EXPOSE 8069 8071 8072
USER odoo

