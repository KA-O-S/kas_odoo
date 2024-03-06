from odoo:17.0
USER root
COPY /home/odoo-docker/odoo_17.0+e.latest_all.deb /tmp/
RUN dpkg -i /tmp/odoo_17.0+e.latest_all.deb
RUN cd /var/lib
RUN mkdir odoo
RUN chown -R odoo:odoo odoo
EXPOSE 9069 9071 9072
USER odoo

