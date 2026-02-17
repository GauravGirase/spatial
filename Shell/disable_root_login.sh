#!/bin/bash
sudo vi /etc/ssh/sshd_config
PermitRootLogin no
sudo systemctl restart sshd
