#!/bin/sh

# 設置變數
backup_dir="/pg_backups"
now=$(date +"%d-%m-%Y_%H-%M")
db_name="5j03wu6"

# 進行數據庫備份
pg_dump -E UTF8 $db_name | gzip > "$backup_dir/backup-$now.tar.gz"
echo "Database backup completed: backup-$now.tar.gz"

# 清理過期的備份文件
find "$backup_dir" -name "*.tar.gz" -type f -mtime +30 -exec rm -f {} \;
echo "Expired backup files deleted."

exit 0
