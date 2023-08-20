#FROM registry.gitlab.com/hav-media/odoo-images/postgres:14.1

# Create Live and Stage Users
COPY ./init/init.sql /docker-entrypoint-initdb.d/

# Set Master Password for Postgres
ENV POSTGRES_PASSWORD "cQFq-ro+tkZau!fbqPbh1o--Y!+A^4dm9oZ@T%_3Mc@"
