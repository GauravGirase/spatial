#!/bin/sh

if [ -d "/dir" ] && [ ! -w "/dir"]; then
    chmod 777 /dir 2>/dev/null || \
      echo "WARN: /dir is not writable by the app user"
fi

'''
[ -d "/dir" ]: true only if /dir exists and is a directory
[ ! -w "/dir"]: true , if current user cannot write it
'''
