FROM postgres:15-alpine

COPY init_scripts/ /docker-entrypoint-initdb.d/

RUN chmod 755 /docker-entrypoint-initdb.d/*.sql

RUN apk add --no-cache tzdata

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD pg_isready -U user -d default_db

EXPOSE 5432

CMD ["postgres"]
