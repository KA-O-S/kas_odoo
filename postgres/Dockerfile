FROM postgres:15.0

# Create Live and Stage Users
COPY ./init/init.sql /docker-entrypoint-initdb.d/

# Set Master Password for Postgres
ENV POSTGRES_PASSWORD "Ur39H&@32Tw&HNGR2UoNgTmaf"
