#!/bin/bash
# Service Auto-Restart Script


SERVICE="filebeat"

if ! systemctl is-active --quiet "$SERVICE"; then
    systemctl restart "$SERVICE"
    echo "$SERVICE restarted at $(date)" >> /var/log/service-monitor.log
fi



############################
# Explanation
############################
# is-active --quiet	--quiet	No output
# restart	Restart service
