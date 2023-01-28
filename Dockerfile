FROM mysql/mysql-server

ENV MYSQL_DATABASE=deutsche_bahn \
    #MYSQL_ROOT_PASSWORD=password \
    MYSQL_ROOT_HOST=%
    MYSQL_ALLOW_EMPTY_PASSWORD= No

ADD schema.sql /docker-entrypoint-initdb.d

EXPOSE 3307