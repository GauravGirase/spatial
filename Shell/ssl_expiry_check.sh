#!/bin/bash
# SSL Expiry Check Script

HOST="example.com"
EXPIRY=$(echo | openssl s_client -servername $HOST -connect $HOST:443 2>/dev/null \
| openssl x509 -noout -enddate | cut -d= -f2)

EXPIRY_DATE=$(date -d "$EXPIRY" +%s)
NOW=$(date +%s)

DAYS_LEFT=$(( (EXPIRY_DATE - NOW) / 86400 ))

if [ "$DAYS_LEFT" -lt 15 ]; then
    echo "SSL expires in $DAYS_LEFT days"
fi



############################
# Explanation
############################
# openssl s_client	-connect	Connect host
# -servername	SNI	
# x509 -noout	No certificate dump	
# -enddate	Show expiry	
