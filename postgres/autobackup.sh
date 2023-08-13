#!/bin/sh

backup_dir="/pg_backups"
now=$(date +"%d-%m-%Y_%H-%M")
db_name="5j03wu6"
pg_dump -E UTF8 $db_name | gzip  > $backup_dir/backup-$now.tar
# remove all files (type f) modified longer than 30 days ago under /pg_backups
find /pg_backups -name "*.sql" -type f -mtime +30 -delete

exit 0
