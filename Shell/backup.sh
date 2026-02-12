#!/bin/bash

set -euo pipefail 

BACKUP_DIR="/backup"
SOURCE_DIR="/var/lib/elasticsearch"
DATE=$(date +%F)
ARCHIVE_NAME="es-backup-$DATE.tar.gz"

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_DIR/$ARCHIVE_NAME" "$SOURCE_DIR"

find "$BACKUP_DIR" -type f -mtime +7 -delete

echo "Backup completed: $ARCHIVE_NAME"

#################################
# Explanation
#################################
# set -e	Exit if any command fails
# set -u	Exit if variable is undefined
# set -o pipefail	Fail if any command in pipe fails
# tar -c	Create archive
# tar -z	Compress using gzip
# tar -f	Filename
# find -mtime +7	Files older than 7 days
# -delete	Delete matched files
