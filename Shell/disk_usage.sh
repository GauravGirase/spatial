#!/bin/bash
# Disk Usage Alert Script

THRESHOLD=80
EMAIL="admin@example.com"

USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "Disk usage is ${USAGE}%" | mail -s "Disk Alert" "$EMAIL"
fi


############################
# Explanation
############################
# df -h	-h	Human readable
# awk 'NR==2'	NR==2	Second row
# sed 's/%//'	Remove %	
# mail -s	-s	Subject
