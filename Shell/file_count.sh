#!/bin/bash

DIR="$1"

if [ -d "$DIR" ]; then
    FILE_COUNT=$(find "$DIR" -maxdepth 1 -type f | wc -l)
    echo "Number of files in '$DIR': $FILE_COUNT"
else
    echo "'$DIR' is not present"
fi
