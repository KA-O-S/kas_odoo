from odoo:16.0
USER root
COPY odoo_16.0+e.latest_all.deb /tmp/
RUN dpkg -i /tmp/odoo_16.0+e.latest_all.deb
RUN cd /var/lib && chown -R odoo:odoo odoo
# Expose Odoo services
EXPOSE 9069 9071 9072
USER odoo

