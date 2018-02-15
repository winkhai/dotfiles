#!/usr/bin/env bash

sh -c 'echo "set const" >> .nanorc'

sh -c 'echo "set tabsize 4" >> .nanorc'

sh -c 'echo "set tabstospaces" >> .nanorc'

adduser --disabled-password --gecos "" new_user

usermod -aG sudo new_user

cp .nanorc /home/new_user/

mkdir -p /etc/ssh