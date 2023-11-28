FROM postgres:14.9-alpine3.17

COPY schema/*.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_DB=5j03wu6
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV TZ="Asia/Taipei"

RUN mkdir /pg_backups && echo "0 0 * * * /etc/periodic/autobackup.sh" >> /var/spool/cron/crontabs/postgres
COPY ./autobackup.sh /etc/periodic/
RUN chmod +x /etc/periodic/autobackup.sh
RUN crond