FROM postgres:15

# Create Live and Stage Users
COPY ./init/init.sql /docker-entrypoint-initdb.d/

# Set Master Password for Postgres
ENV POSTGRES_PASSWORD "h6<%.#<E2@?6(T,&jY!p,$(<XQ&DM5u}3§"
