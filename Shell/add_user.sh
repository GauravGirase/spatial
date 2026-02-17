#!/bin/bash

USERNAME="$1"
PASSWORD="$2"

if id "$USERNAME" &>/dev/null; then
    echo "User already exists"
else
    sudo useradd -m "$USERNAME"
    echo "$USERNAME:$PASSWORD" | sudo chpasswd
    echo "User created successfully"
fi
